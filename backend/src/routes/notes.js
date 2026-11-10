const express = require("express");
const db = require("../db");
const auth = require("../middleware/auth");

const router = express.Router();
router.use(auth); // every notes route needs a valid token

// Checks title/content before saving
const validate = (req, res, next) => {
  const { title, content } = req.body || {};
  if (!title || !title.trim() || !content || !content.trim()) {
    return res.status(400).json({ error: { message: "Title and content are required" } });
  }
  if (title.length > 200) {
    return res.status(400).json({ error: { message: "Title must be 200 characters or less" } });
  }
  next();
};

// Every query filters by req.userId, so users only touch their own notes
router.get("/", async (req, res) => {
  const [notes] = await db.query(
    "SELECT id, title, content, created_at, updated_at FROM notes WHERE user_id = ? ORDER BY updated_at DESC",
    [req.userId]
  );
  res.json({ notes });
});

router.get("/:id", async (req, res) => {
  const [rows] = await db.query(
    "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ? AND user_id = ?",
    [req.params.id, req.userId]
  );
  if (rows.length === 0) {
    return res.status(404).json({ error: { message: "Note not found" } });
  }
  res.json({ note: rows[0] });
});

router.post("/", validate, async (req, res) => {
  const { title, content } = req.body;
  const [result] = await db.query(
    "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
    [req.userId, title.trim(), content.trim()]
  );
  res.status(201).json({ note: { id: result.insertId, title, content } });
});

router.put("/:id", validate, async (req, res) => {
  const { title, content } = req.body;
  const [result] = await db.query(
    "UPDATE notes SET title = ?, content = ? WHERE id = ? AND user_id = ?",
    [title.trim(), content.trim(), req.params.id, req.userId]
  );
  if (result.affectedRows === 0) {
    return res.status(404).json({ error: { message: "Note not found" } });
  }
  res.json({ message: "Note updated" });
});

router.delete("/:id", async (req, res) => {
  const [result] = await db.query(
    "DELETE FROM notes WHERE id = ? AND user_id = ?",
    [req.params.id, req.userId]
  );
  if (result.affectedRows === 0) {
    return res.status(404).json({ error: { message: "Note not found" } });
  }
  res.json({ message: "Note deleted" });
});

module.exports = router;

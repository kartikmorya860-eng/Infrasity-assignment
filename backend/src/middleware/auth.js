const jwt = require("jsonwebtoken");

// Reads "Authorization: Bearer <token>" and sets req.userId
module.exports = (req, res, next) => {
  const header = req.headers.authorization || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;

  if (!token) {
    return res.status(401).json({ error: { message: "Please log in" } });
  }

  try {
    req.userId = jwt.verify(token, process.env.JWT_SECRET).userId;
    next();
  } catch {
    res.status(401).json({ error: { message: "Invalid or expired token" } });
  }
};

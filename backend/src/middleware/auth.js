const jwt = require("jsonwebtoken");

// Read the bearer token and attach its user ID to the request.
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

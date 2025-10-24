const express = require("express");
const cors = require("cors");
const multer = require("multer");
const { exec } = require("child_process");
const path = require("path");
const app = express();

app.use(cors());
app.use(express.json());

// Storage setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, Date.now() + path.extname(file.originalname))
});
const upload = multer({ storage });

// Upload route
app.post("/upload", upload.single("resume"), (req, res) => {
  const filePath = req.file.path;

  // Run Python script to evaluate
  exec(`python ${__dirname}/ai_model.py ${filePath}`, (error, stdout, stderr) => {
    if (error) return res.status(500).json({ error: stderr });
    const result = JSON.parse(stdout);
    res.json(result);
  });
});

app.listen(5000, () => console.log("Backend running on port 5000"));

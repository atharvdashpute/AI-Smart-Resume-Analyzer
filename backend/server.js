const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: "uploads/" });

app.post("/analyze", upload.single("resume"), async (req, res) => {
  try {
    const jobDescription = req.body.job_description;
    const resumePath = path.resolve(req.file.path); // ✅ FIX

    const response = await axios.post("http://127.0.0.1:5000/analyze", {
      resume_path: resumePath,
      job_description: jobDescription
    });

    res.json(response.data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "AI Engine error" });
  }
});

app.listen(3001, () => {
  console.log("Backend running on port 3001");
});

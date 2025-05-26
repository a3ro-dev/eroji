# 🎭 Eroji - AI Face Analysis App

## Overview

Eroji is an elegant, modern web application that leverages OpenAI's GPT-4.1 Vision capabilities to provide detailed face analysis from uploaded images. The app features a polished, responsive UI built with Streamlit and custom CSS styling.

## ✨ Key Features

### 🧠 Powered by GPT-4.1 Vision
- **No dependencies on traditional computer vision libraries** (OpenCV, DeepFace, etc.)
- **State-of-the-art analysis** leveraging GPT-4.1's powerful vision capabilities
- **JSON-structured responses** for consistent data handling

### 📊 Comprehensive Face Analysis
- **Primary and secondary emotions** with confidence scores
- **Emotional intensity** and expression details
- **Age estimation** with confidence ranges
- **Gender perception** with confidence metrics
- **Ethnicity/race perception** (when detectable)
- **Facial attributes** (hair, facial hair, glasses, accessories)
- **Pose and positioning** analysis
- **Face quality metrics** (visibility, lighting)

### 🎨 Modern UI/UX
- **Clean, polished interface** with custom styling
- **Dark/Light theme support** via Streamlit's theme toggle
- **Responsive design** that works on various screen sizes
- **Interactive elements** with visual feedback
- **Progress indicators** during analysis
- **Detailed result cards** with organized metrics
- **Raw JSON data access** for developers

### 👥 Multi-Face Support
- **Handles multiple faces** in a single image
- **Individual analysis** for each detected face
- **Numerical identification** to distinguish between faces

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key with GPT-4.1 Vision access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/a3ro-dev/eroji.git
   cd eroji
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key:**
   - Create a `.streamlit/secrets.toml` file with:
     ```toml
     OPENAI_API_KEY = "sk-your-api-key-here"
     ```
   - Or set it as an environment variable:
     ```bash
     export OPENAI_API_KEY=sk-your-api-key-here
     ```

### Running the App

```bash
streamlit run app.py
```

The app will be accessible at `http://localhost:8501` in your web browser.
- **Static Image Analysis** - Analyze any image file
- **Interactive Menu** - User-friendly navigation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to the [GitHub repository](https://github.com/a3ro-dev/eroji).

---

**Made with ❤️ by [a3ro-dev](https://github.com/a3ro-dev)**

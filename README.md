# Sentiment-Analysis-of-E-Commerce-Customer-Reviews

# 🚀 Flipkart Product Review Sentiment Analyzer

Welcome to the **Flipkart Product Review Sentiment Analyzer** — a powerful tool that automates the scraping of Flipkart reviews, analyzes sentiments and ratings, and presents the data on a modern web interface built with Flask.

---

## 📌 Table of Contents

- [📂 Project Structure](#-project-structure)
- [⚙️ Requirements](#️-requirements)
- [🚀 How to Run](#-how-to-run)
- [🧠 Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🛠️ To-Do](#️-to-do)
- [📄 License](#-license)

---
## Screenshot ##
![Live Demo Screenshot](https://github.com/SurajZagare/Sentiment-Analysis-of-E-Commerce-Customer-Reviews/blob/0e456f745ea18335b72f825070e1c28b6695aeb6/Screenshot%202025-04-04%20143657.png)
![Live Demo Screenshot](https://github.com/SurajZagare/Sentiment-Analysis-of-E-Commerce-Customer-Reviews/blob/0e456f745ea18335b72f825070e1c28b6695aeb6/Screenshot%202025-04-04%20143714.png)
![Live Demo Screenshot](https://github.com/SurajZagare/Sentiment-Analysis-of-E-Commerce-Customer-Reviews/blob/0e456f745ea18335b72f825070e1c28b6695aeb6/Screenshot%202025-04-04%20143743.png)
![Live Demo Screenshot](https://github.com/SurajZagare/Sentiment-Analysis-of-E-Commerce-Customer-Reviews/blob/0e456f745ea18335b72f825070e1c28b6695aeb6/Screenshot%202025-04-04%20143805.png)
![Live Demo Screenshot](https://github.com/SurajZagare/Sentiment-Analysis-of-E-Commerce-Customer-Reviews/blob/0e456f745ea18335b72f825070e1c28b6695aeb6/Screenshot%202025-04-04%20143828.png)
>
## ⚙️ Requirements


Make sure Python 3.7+ is installed. Then install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```txt
flask
requests
beautifulsoup4
firebase-admin
textblob
```

---

## 🔧 Firebase Setup

1. Visit [Firebase Console](https://console.firebase.google.com/)
2. Create a project
3. Navigate to **Project Settings > Service Accounts** and generate a key
4. Download the JSON key and save it as `firebase/service.json`
5. In Firebase Realtime Database settings, set database rules to allow read/write or authenticate as required.

---

## 🚀 How to Run

### Step 1: Run Automation Script

```bash
cd automation
python automation.py
```

- Input:
  - Flipkart review URL
  - Flipkart product page URL
- Output:
  - Analyzed data with average rating and overall sentiment
  - Data saved to Firebase

### Step 2: Run Flask Web App

```bash
cd ../website
python app.py
```

Then open your browser and go to:
```
http://127.0.0.1:5000/
```

---

## 🧠 Features

✅ Automated scraping of Flipkart reviews  
✅ Sentiment analysis and average rating extraction  
✅ Data storage using Firebase  
✅ Flask-based web interface for visual output  
✅ Real-time product search and filtering

---

## 📸 Screenshots

> *(Add screenshots here after running the app)*

---

## 🛠️ To-Do

- [ ] Add sentiment-based product filtering
- [ ] Pagination for long product listings
- [ ] Dockerize for easier deployment
- [ ] Add real-time review updates

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgments

- [Flipkart](https://www.flipkart.com/) for being a data source
- [Firebase](https://firebase.google.com/) for backend hosting
- OpenAI ChatGPT for project documentation help 😄

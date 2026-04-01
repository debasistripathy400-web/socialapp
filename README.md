# 📸 SocialApp - Premium Django Social Platform

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Framework-Django-092e20.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Language-Python-3776ab.svg)](https://www.python.org/)

**SocialApp** is a feature-rich, Instagram-inspired social media platform built with Django. It delivers a modern, high-performance UI balanced with professional-grade privacy and content management features.

---

## ✨ Immersive Features

### 🎞️ Immersive Story Viewer
- **Active Stories Stream**: A sleek, horizontally scrollable bar for active highlights.
- **Narrative Navigation**: Integrated Tap-to-Navigate (Forward/Backward) and Auto-Progress timers.
- **Story Management**: Easy deletion for active highlights directly from the viewer.

### 🖼️ High-End Feed & Content
- **Responsive Media Grid**: A beautiful, triple-column profile grid for high-resolution content.
- **Post-Level Control**: Edit or Delete your posts with a discrete management ellipsis menu.
- **Post Zoom View**: Dedicated detail screens for every post with full caption and comment support.

### 🛡️ Privacy & Security Suite
- **Account Toggling**: Instantly switch between **Public** and **Private** account status.
- **Integrated Lock Screen**: Private profiles are automatically shielded with a custom lock screen for non-followers.
- **Feed Shield**: Content from private accounts is intelligently filtered from global feeds.

### 🔔 Activity Feed
- **Real-Time Notifications**: Instant alerts for New Followers, Likes, and Comments.
- **User Discovery**: Modern search engine to find and follow your friends.

---

## 🛠️ Technical Stack
- **Backend**: Python 3.x, Django 5.x
- **Database**: SQLite (Development)
- **Frontend**: Vanilla CSS, HTML5, JavaScript (AJAX, DOM Manipulation)
- **Icons**: FontAwesome 6 (Pro Icons)
- **Fonts**: Google Fonts (Inter)

---

## ⚡ Quick Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/debasistripathy400-web/socialapp.git
   cd socialapp
   ```

2. **Setup Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django pillow
   ```

4. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   *Visit `http://127.0.0.1:8000/` to start sharing!*

---

## 📜 License
Licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing
Contributions are welcome! If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

**Developed by [Debasis Tripathy](https://github.com/debasistripathy400-web)**

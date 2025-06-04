# VenvDez_FLASK

**Empower Your Data, Simplify Your Decisions**

![Last Commit](https://img.shields.io/github/last-commit/yourusername/VenvDez_FLASK?label=last%20commit&color=brightgreen) ![Python](https://img.shields.io/badge/python-61.7%25-blue) ![Languages](https://img.shields.io/github/languages/count/yourusername/VenvDez_FLASK)

---

## Overview

VenvDez_FLASK is a powerful Flask-based web application designed to streamline data management and enhance user interaction with complex datasets. It provides an intuitive, responsive interface backed by automated backup, smart attendance tracking, and dynamic visualizations.

### Why VenvDez_FLASK?

This project empowers developers and administrators to manage data efficiently while ensuring data integrity and user engagement. The core features include:

- 📦 **Automated Backup Management**  
  Ensures data integrity and availability through scheduled backups, preventing data loss.

- 🌐 **User-Friendly Data Interface**  
  Simplifies interactions with complex datasets via an intuitive web interface.

- 🧠 **Natural Language Processing (NLP)**  
  Enhances data analysis capabilities for sophisticated text-based analytics.

- 📊 **Interactive Data Visualization**  
  Utilizes Plotly for dynamic visualizations, making data interpretation easier.

- 📱 **Responsive Design**  
  Ensures accessibility across devices, improving overall user experience.

- 🗂️ **Attendance Management**  
  Streamlines the entry and tracking of attendance records, simplifying administrative tasks.

---

## Table of Contents

1. [Features](#features)  
2. [Demo Screenshots](#demo-screenshots)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Configuration](#configuration)  
6. [Directory Structure](#directory-structure)  
7. [Deployment](#deployment)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Features

1. **Automated Backup Management**  
   - Runs scheduled monthly and quarterly backups of the Access database.  
   - Logs backup metadata and prevents redundant backups for the same period.  
   - Automatically synchronizes hidden and main database files (RAID-style failover).

2. **User-Friendly Data Interface**  
   - Filterable data tables by site, company, name, presence type, month, and year.  
   - Multi-select dropdowns powered by Select2 and Flatpickr date range selection.  
   - Sticky headers, infinite scroll, and dynamic chart resizing based on screen width.

3. **Natural Language Processing (NLP)**  
   - Integrated NLTK for tokenization, stopword removal, and POS tagging.  
   - Chatbot interface supports greetings, presence-related questions, and CRUD guidance.  
   - Customizable intent/response mapping for common user inquiries.

4. **Interactive Data Visualization**  
   - Plotly scatter, pie, and stacked bar charts show presence distribution and trends.  
   - Scatter plot tooltips display “Substituição” events with hover details (who substituted whom).  
   - Responsive resizing logic captures screen width on page load for optimal chart dimensions.

5. **Responsive Design**  
   - Tailwind/CSS variables for light/dark mode toggling.  
   - Fluid layout ensures usability on desktops, tablets, and mobile devices.  
   - Adaptive menu, sidebar, and form components with smooth theme transitions.

6. **Attendance Management**  
   - Add/Remove presence entries per user, with hidden “substitution” type insertion logic.  
   - Historical view of current month’s records and real-time chart updates.  
   - Add/Reactivate/Deactivate users and companies directly from the “Adicionar Presença” page.

---

## Demo Screenshots

> *Preview of the home page with filters and charts*  
![Home Page Preview](docs/screenshots/home_preview.png)  

> *“Adicionar Presença” page with attendance form and substitution widget*  
![Adicionar Presença Preview](docs/screenshots/add_presence_preview.png)  

> *Scatter plot showing “Substituição” tooltips*  
![Scatter Plot with Tooltip](docs/screenshots/scatter_tooltip.png)  

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/VenvDez_FLASK.git
   cd VenvDez_FLASK
   ```

2. **Create a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**  
   The app auto-checks and installs required NLTK corpora (punkt, stopwords, etc.) on first run.  
   Optionally, you can manually download by running:
   ```bash
   python - <<EOF
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('averaged_perceptron_tagger_eng')
   EOF
   ```

5. **Prepare the Access database**  
   - Ensure `Controle_Frequencia.accdb` is placed under `database/` folder.  
   - If not present, copy your existing DB or run the provided SQL migration scripts (if any).

---

## Usage

1. **Set the secret key**  
   Edit `appFlask.py` and modify `app.secret_key = "your-unique-secret"` if desired.

2. **Run the Flask server**  
   ```bash
   flask run
   ```
   By default, the app listens on `http://127.0.0.1:5000/`.

3. **Open in your browser**  
   Navigate to `http://127.0.0.1:5000/` to view the main dashboard.

4. **Navigate features**  
   - Use the sidebar to select a **Site** and **Empresa**.  
   - Filter attendance records by name, presence type, month, or year.  
   - Click **“Adicionar Presença”** to add, remove, or substitute presence.  
   - Manage users (add, activate, deactivate) and companies directly from the form panels.

5. **Chatbot**  
   - Click the 💬 icon in the bottom corner to open the chat widget.  
   - Ask questions like “Como adiciono uma presença?” or “Quero ver nomes cadastrados”.  
   - The bot uses NLTK-powered intent matching to provide relevant guidance.

---

## Configuration

- **Database Path**  
  Default: `database/Controle_Frequencia.accdb`  
  To point to a different file, modify `backup_manager.py` and `get_db_connection()` in `appFlask.py`.

- **Backup Schedule**  
  The backup logic runs automatically on the 1st of each month (and quarterly).  
  To test or override dates, adjust `backup_manager.verificar_data_e_fazer_backup()`.

- **Theme (Light/Dark)**  
  The CSS variables in `static/styles.css` handle both light and dark mode.  
  Toggle with the button labeled “Alternar Tema” in the sidebar.

- **NLTK Downloads**  
  By default, the code calls `verificar_e_instalar_nltk()` at startup.  
  To disable auto-downloading, comment out the call in `appFlask.py`.

---

## Directory Structure

```
VenvDez_FLASK/
├── appFlask.py               # Main Flask application
├── backup_manager.py         # Backup & synchronization logic
├── requirements.txt          # Python dependencies
├── database/
│   ├── Controle_Frequencia.accdb  # Primary Access DB
│   └── Controle_Frequencia_oculto.accdb  # Hidden mirror copy
├── static/
│   ├── styles.css            # Global CSS (light/dark mode)
│   └── …                     # JS libraries, images, icons
├── templates/
│   ├── index.html            # Main dashboard template
│   ├── adicionar_presenca.html  # Add / substitute presence
│   └── …                     # Other partials & forms
├── docs/
│   ├── screenshots/          # Demo screenshot images
│   └── …                     # Additional documentation or diagrams
└── test_substituicoes.py     # Standalone test for SQL query debugging
```

---

## Deployment

1. **Windows + IIS / Apache**  
   - Install Python 3.8+ and ODBC driver for Access.  
   - Configure your WSGI entry point to `appFlask.app`.  
   - Set environment variable:
     ```
     set FLASK_APP=appFlask.py
     set FLASK_ENV=production
     ```
   - Configure scheduled tasks or Windows Scheduler to run `backup_manager.verificar_data_e_fazer_backup()` monthly (optional).

2. **Linux + Apache (mod_wsgi)**  
   - Copy `Controle_Frequencia.accdb` into a directory accessible by the web server (ensure read/write permissions).  
   - Install `unix-odbc` and `msodbcsql17` (or the appropriate ODBC driver for Access via `mdbtools`/`ODBC Bridge`).  
   - Configure `wsgi.conf`:
     ```apache
     WSGIDaemonProcess VenvDez_FLASK python-path=/path/to/VenvDez_FLASK/venv/lib/python3.x/site-packages
     WSGIScriptAlias / /path/to/VenvDez_FLASK/appFlask.wsgi
     <Directory /path/to/VenvDez_FLASK>
         Require all granted
     </Directory>
     ```
   - In `appFlask.wsgi`:
     ```python
     import sys
     sys.path.insert(0, "/path/to/VenvDez_FLASK")
     from appFlask import app as application
     ```

3. **Heroku / Cloud Hosting** _(not recommended for MS Access)_  
   - Convert Access DB → PostgreSQL or SQLite first.  
   - Adjust `get_db_connection()` to point to the new database.  
   - Deploy via `Procfile`:
     ```
     web: gunicorn appFlask:app
     ```

---

## Contributing

We welcome contributions! To submit a pull request:

1. Fork the repository.  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/awesome-feature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add awesome feature"
   ```
4. Push to your branch:  
   ```bash
   git push origin feature/awesome-feature
   ```
5. Open a Pull Request at GitHub, describing the new feature or bug fix.

Please ensure:
- Code follows PEP8 style guidelines.  
- New dependencies are added to `requirements.txt`.  
- You update this README if you introduce new functionality or break backward compatibility.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

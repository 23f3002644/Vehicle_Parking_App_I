# 🚗 Vehicle Parking App

A multi-user parking management web application built with **Flask**, **SQLAlchemy**, **SQLite**, **Jinja2**, and **HTML/CSS**.

The app supports separate admin and user workflows, allowing lot management, booking, release, and reservation history.

---

## ✨ Features

- Admin can add, edit, and delete parking lots.
- Manage spot count per lot and set lot pricing.
- User registration and login.
- Book a parking spot automatically using the first available spot.
- Release/vacate booked parking spots.
- View reservation summaries, history, and lot details.

---

## 📁 Project Structure

```
Vehicle_Parking_App_I/
├── app.py
├── requirement.txt
├── application/
│   ├── controllers.py
│   ├── database.py
│   └── models.py
├── templates/
│   ├── add_lot.html
│   ├── admin_dash.html
│   ├── admin_user.html
│   ├── all_reserve.html
│   ├── Booking.html
│   ├── delete_spot.html
│   ├── edit_lot.html
│   ├── edit_user_prof.html
│   ├── invalid_login.html
│   ├── login.html
│   ├── parking_spot_details.html
│   ├── register.html
│   ├── release.html
│   ├── search.html
│   ├── summ_admin.html
│   ├── summ_user.html
│   └── user_dash.html
├── static/
│   └── css/
│       └── style.css
├── instance/
│   └── parking.sqlite3
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd Vehicle_Parking_App_I
   ```

2. Create a virtual environment:
   ```sh
   python -m venv myenv
   ```

3. Activate the virtual environment:
   ```sh
   myenv\Scripts\activate
   ```

4. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```

5. Run the application:
   ```sh
   python app.py
   ```

6. Open the app in a browser:
   ```sh
   http://127.0.0.1:5000/
   ```

---

## 🗄️ Database

- Database engine: **SQLite**
- File location: `instance/parking.sqlite3`
- Uses **Flask SQLAlchemy** for ORM mapping
- Tables are created automatically when the app runs

---

## 👥 User Roles

### Admin
- Admin account is created automatically.
- Manage parking lots and spot availability.
- View all users and reservation summaries.

### Registered User
- Register and log in.
- Search and book parking lots.
- Release booked spots.
- View booking history.

---

## 🚀 Notes for GitHub

- Rename `requirement.txt` to `requirements.txt` for standard pip usage if desired.
- Add a `.gitignore` file to exclude `myenv/`, `__pycache__/`, and `instance/*.sqlite3`.
- Keep the SQLite database local for development only.

---

## 📌 License

This project is intended for learning and demonstration purposes.

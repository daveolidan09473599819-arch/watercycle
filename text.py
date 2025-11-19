import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🌱 Smart Irrigation System", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
    body { background: #f7f9fb; font-family: 'Poppins', sans-serif; }
    .app-header {
        background: linear-gradient(90deg, #2a9d8f, #264653);
        color: white;
        padding: 20px 40px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 25px;
    }
    .app-header h1 { font-size: 1.8rem; font-weight: 700; margin: 0; }
    .logout-btn {
        background: #e76f51; color: white; border: none; border-radius: 8px;
        padding: 8px 16px; font-weight: 600; cursor: pointer; transition: 0.3s;
    }
    .logout-btn:hover { background: #d65c40; }
    .card {
        background: white; padding: 25px; border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        text-align: center; transition: transform 0.2s ease-in-out;
    }
    .card:hover { transform: translateY(-5px); }
    .metric-title { color: #264653; font-weight: 600; font-size: 1.1rem; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #2a9d8f; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #a8edea 0%, #fed6e3 100%);
    }
    .stButton>button {
        background-color: #2a9d8f; color: white; border-radius: 8px; border: none;
        padding: 10px 20px; font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1f776d; color: #dff3f1; }
    </style>
""", unsafe_allow_html=True)

# ------------------ SENSOR SIMULATION ------------------
def get_soil_moisture(location):
    base = {"Farm A": 40, "Farm B": 25, "Farm C": 50}.get(location, 35)
    return random.uniform(base - 10, base + 10)

def get_water_level(location):
    base = {"Farm A": 3000, "Farm B": 1500, "Farm C": 4500}.get(location, 2000)
    return random.uniform(base - 500, base + 500)

def get_weather_conditions(location):
    weather_by_location = {
        "Farm A": ['Sunny', 'Cloudy', 'Rainy'],
        "Farm B": ['Sunny', 'Storm', 'Cloudy'],
        "Farm C": ['Rainy', 'Cloudy', 'Sunny']
    }
    return random.choice(weather_by_location.get(location, ['Sunny', 'Cloudy']))

def predict_water_need(weather, soil_moisture):
    if weather == 'Rainy': return max(0, 50 - soil_moisture)
    elif weather == 'Sunny': return max(0, 70 - soil_moisture)
    elif weather == 'Storm': return 0
    else: return max(0, 60 - soil_moisture)

def automate_irrigation(water_level, water_needed):
    min_water_level = 1500
    water_per_application = 100
    if water_level > min_water_level and water_needed > 10:
        if water_level >= water_per_application:
            st.success(f"✅ Irrigation started. Dispensing {water_per_application} liters of water.")
            water_level -= water_per_application
        else:
            st.warning("⚠️ Not enough water to irrigate.")
    else:
        st.info("ℹ️ Conditions not suitable or water too low.")
    return water_level

def send_notification(message):
    st.error(f"🚨 Notification: {message}")

# ------------------ AUTH SYSTEM ------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

def signup():
    st.subheader("📝 Create an Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if username in st.session_state.users:
            st.warning("⚠️ Username already exists.")
        elif username and password:
            st.session_state.users[username] = password
            st.success("✅ Account created! Please log in.")
        else:
            st.error("❌ Please enter both username and password.")

def login():
    st.subheader("🔐 Log In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in_user = username
            st.success(f"✅ Welcome back, {username}!")
        else:
            st.error("❌ Invalid username or password.")

def logout():
    st.session_state.logged_in_user = None
    st.info("👋 You have been logged out.")

# ------------------ AUTH HANDLER ------------------
if not st.session_state.logged_in_user:
    auth_choice = st.sidebar.radio("Account Access", ["Login", "Sign Up"])
    if auth_choice == "Login":
        login()
    else:
        signup()
    st.stop()

# ------------------ HEADER ------------------
st.markdown(f"""
<div class="app-header">
    <h1>🌾 Smart Irrigation Monitoring System</h1>
    <form action="#" method="post">
        <button class="logout-btn" type="submit" onClick="window.location.reload();">🚪 Logout</button>
    </form>
</div>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Farm Settings")
location = st.sidebar.selectbox("Select Farm Location", ["Farm A", "Farm B", "Farm C"])
st.sidebar.info(f"Monitoring active for: **{location}**")

# Initialize state
if "water_levels" not in st.session_state:
    st.session_state.water_levels = {loc: get_water_level(loc) for loc in ["Farm A", "Farm B", "Farm C"]}
if "schedules" not in st.session_state:
    st.session_state.schedules = []  # store as list of dicts

current_water_level = st.session_state.water_levels[location]

# ------------------ DASHBOARD ------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="card"><p class="metric-title">💧 Water Level</p>
    <p class="metric-value">{current_water_level:.2f} L</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="card"><p class="metric-title">📍 Location</p>
    <p class="metric-value">{location}</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="card"><p class="metric-title">👤 User</p>
    <p class="metric-value">{st.session_state.logged_in_user}</p></div>""", unsafe_allow_html=True)

# ------------------ SCHEDULING SYSTEM ------------------
st.markdown("### 🕒 Irrigation Scheduling System")

# Add new schedule
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    schedule_date = st.date_input("Select Date", datetime.now().date())
with col2:
    schedule_time = st.time_input("Select Time", datetime.now().time())
with col3:
    if st.button("➕ Add Schedule"):
        new_schedule = {
            "Location": location,
            "Datetime": datetime.combine(schedule_date, schedule_time),
            "Status": "Pending"
        }
        st.session_state.schedules.append(new_schedule)
        st.success("✅ Schedule added successfully!")

# Display all schedules
if st.session_state.schedules:
    df = pd.DataFrame(st.session_state.schedules)
    st.dataframe(df, use_container_width=True)

    # Delete old schedules
    if st.button("🗑️ Clear All Schedules"):
        st.session_state.schedules.clear()
        st.warning("All schedules removed.")
else:
    st.info("No schedules available. Add one above.")

# ------------------ RUN AUTOMATED SCHEDULES ------------------
now = datetime.now()
for sched in st.session_state.schedules:
    if sched["Status"] == "Pending" and now >= sched["Datetime"]:
        st.info(f"🚀 Running scheduled irrigation for {sched['Location']}...")
        soil_moisture = get_soil_moisture(sched["Location"])
        weather = get_weather_conditions(sched["Location"])
        water_needed = predict_water_need(weather, soil_moisture)
        st.session_state.water_levels[sched["Location"]] = automate_irrigation(
            st.session_state.water_levels[sched["Location"]], water_needed
        )
        sched["Status"] = "Completed"
        st.success(f"✅ Irrigation completed for {sched['Location']} at {now.strftime('%H:%M:%S')}")

# ------------------ MANUAL RUN ------------------
st.markdown("### 🔄 Manual Monitoring")
if st.button("Run Now"):
    soil_moisture = get_soil_moisture(location)
    weather = get_weather_conditions(location)
    water_needed = predict_water_need(weather, soil_moisture)
    new_water_level = automate_irrigation(current_water_level, water_needed)
    st.session_state.water_levels[location] = new_water_level
# ------------------ RUN AUTOMATED SCHEDULES ------------------
now = datetime.now()
for sched in st.session_state.schedules:
    # 🔔 If schedule is due now, run it
    if sched["Status"] == "Pending" and now >= sched["Datetime"]:
        time_diff = (now - sched["Datetime"]).total_seconds() / 60  # minutes difference

        if time_diff <= 5:  # allow a 5-minute grace period
            st.info(f"🚀 Running scheduled irrigation for {sched['Location']}...")
            soil_moisture = get_soil_moisture(sched["Location"])
            weather = get_weather_conditions(sched["Location"])
            water_needed = predict_water_need(weather, soil_moisture)
            st.session_state.water_levels[sched["Location"]] = automate_irrigation(
                st.session_state.water_levels[sched["Location"]], water_needed
            )
            sched["Status"] = "Completed"
            st.success(f"✅ Irrigation completed for {sched['Location']} at {now.strftime('%H:%M:%S')}")
        else:
            # 🔔 Added alert for missed schedule
            st.warning(
                f"⚠️ ALERT: Irrigation for **{sched['Location']}** was scheduled at "
                f"{sched['Datetime'].strftime('%Y-%m-%d %H:%M:%S')} and has been missed by "
                f"{int(time_diff)} minutes."
            )
            sched["Status"] = "Missed"


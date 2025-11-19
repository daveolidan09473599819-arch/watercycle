import streamlit as st
import random
from datetime import datetime
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="🌱 Smart Irrigation System", layout="wide")

# ------------------ STYLE ------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images8.alphacoders.com/108/1088470.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.85);
    z-index: -1;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #4CBB17, #2E8B57);
}
.main-content {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
* { font-family: 'Poppins', sans-serif; }
.app-header {
    background: linear-gradient(90deg, #6B8E23, #8FBC8F);
    color: #fff;
    padding: 20px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}
.app-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
}
.red-delete-btn > button {
    background-color: #FF0000 !important;
    color: red !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 6px 14px !important;
    font-weight: 600 !important;
    transition: 0.3s !important;
}
.red-delete-btn > button:hover {
    background-color: #b71c1c !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------ SENSOR + AI FUNCTIONS ------------------
def get_sensor_data():
    soil = random.uniform(30, 60)
    temp = random.uniform(25, 35)
    humidity = random.uniform(55, 80)
    water = random.uniform(2000, 4000)
    weather = random.choice(["Sunny", "Cloudy", "Rainy", "Storm"])
    return soil, temp, humidity, water, weather

def predict_water_need(weather, soil, crop_type):
    crop_factor = {"Rice": 70, "Corn": 60, "Vegetables": 55}
    base = crop_factor.get(crop_type, 60)
    if weather == "Rainy": return max(0, base - soil - 10)
    elif weather == "Sunny": return max(0, base - soil + 10)
    elif weather == "Cloudy": return max(0, base - soil)
    else: return 0

def generate_recommendation(water_need):
    if water_need <= 0:
        return "💧 No irrigation needed today. Soil moisture is sufficient."
    elif water_need < 20:
        return "💧 Minimal irrigation needed — monitor soil moisture."
    elif water_need < 40:
        return "💦 Moderate irrigation recommended for optimal growth."
    else:
        return "🚿 High irrigation required! Soil is too dry."

# ------------------ AUTH SYSTEM ------------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "farms" not in st.session_state:
    st.session_state.farms = []
if "harvest_results" not in st.session_state:
    st.session_state.harvest_results = []

def signup():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.subheader("Create Account")
    user = st.text_input("Username", key="signup_user")
    pw = st.text_input("Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["User", "Admin"], key="signup_role")
    if st.button("Sign Up"):
        if user in st.session_state.users:
            st.warning("⚠️ Username already exists.")
        elif user and pw:
            st.session_state.users[user] = {"password": pw, "role": role}
            st.success(f"✅ {role} account created! Please log in.")
        else:
            st.error("❌ Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

def login():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.subheader("Log In")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        if user in st.session_state.users and st.session_state.users[user]["password"] == pw:
            st.session_state.logged_in_user = user
            st.success(f"✅ Welcome, {user}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.logged_in_user = None
    st.success("Logged out successfully!")
    st.rerun()

# ------------------ LOGIN / SIGNUP ------------------
if not st.session_state.logged_in_user:
    auth = st.sidebar.radio("Account Access", ["Login", "Sign Up"])
    login() if auth == "Login" else signup()
    st.stop()

current_user = st.session_state.logged_in_user
role = st.session_state.users[current_user]["role"]

# ------------------ HEADER ------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="app-header"><h1>AI-Powered Smart Irrigation System</h1></div>', unsafe_allow_html=True)
with col2:
    st.button("Logout", on_click=logout, key="logout_btn", use_container_width=True)

# ------------------ ADMIN VIEW ------------------
if role == "Admin":
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.subheader("Admin Dashboard")

    # USERS TABLE
    st.markdown("### 👥 Registered Users")
    if st.session_state.users:
        df_users = pd.DataFrame([{"Username": u, "Role": d["role"]} for u, d in st.session_state.users.items()])
        st.dataframe(df_users, use_container_width=True)

        for username, data in st.session_state.users.copy().items():
            cols = st.columns([4, 1])
            cols[0].write(f"👤 *{username}* ({data['role']})")
            with cols[1]:
                if data["role"] != "Admin":
                    with st.container():
                        if st.button("🗑️ Delete", key=f"del_user_{username}", use_container_width=True):
                            del st.session_state.users[username]
                            st.success(f"✅ Deleted '{username}'")
                            st.rerun()
        st.divider()
    else:
        st.info("No registered users yet.")

    # FARMS TABLE
    st.markdown("### 🌾 Registered Farms")
    if st.session_state.farms:
        st.dataframe(pd.DataFrame(st.session_state.farms), use_container_width=True)
        for i, farm in enumerate(st.session_state.farms):
            cols = st.columns([4, 1])
            cols[0].write(f"🌱 *{farm['Farm Name']}* - {farm['Farmer Name']} ({farm['Barangay']})")
            with cols[1]:
                if st.button("🗑️ Delete", key=f"del_farm_{i}", use_container_width=True):
                    st.session_state.farms.pop(i)
                    st.success(f"✅ Deleted farm '{farm['Farm Name']}'")
                    st.rerun()
        st.divider()
    else:
        st.info("No farms registered yet.")

    # HARVEST RESULTS TABLE
    st.markdown("### 🤖 AI Harvest Analysis")
    if st.session_state.harvest_results:
        st.dataframe(pd.DataFrame(st.session_state.harvest_results), use_container_width=True)
        for i, res in enumerate(st.session_state.harvest_results):
            cols = st.columns([4, 1])
            cols[0].write(f"🌾 *{res['Farm Name']}* ({res['Crop Type']}) - {res['Owner']}")
            with cols[1]:
                if st.button("🗑️ Delete", key=f"del_analysis_{i}", use_container_width=True):
                    st.session_state.harvest_results.pop(i)
                    st.success(f"✅ Deleted analysis for '{res['Farm Name']}'")
                    st.rerun()
    else:
        st.info("No AI harvest results yet.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ------------------ USER VIEW ------------------
st.sidebar.title("🏡 Farm Registration")
barangays = ["Poblacion", "Dugsangon", "Pongtud", "Campo", "Pautao", "Cabugao", "Payapag", "Sto. Rosario", "Cambuayon"]

with st.sidebar.expander("➕ Register New Farm"):
    farmer_name = st.text_input("👨‍🌾 Name of Farmer")
    purok = st.text_input("🏘️ Purok")
    farm_name = st.text_input("🌾 Farm Name")
    barangay = st.selectbox("📍 Barangay", barangays)
    crop_type = st.selectbox("🌱 Crop Type", ["Rice", "Corn", "Vegetables"])
    area = st.number_input("📏 Area Size (hectares)", 0.1, 100.0, 1.0)
    planting_start = st.date_input("🗓️ Start of Planting")

    if st.button("Register Farm"):
        if farm_name and farmer_name:
            st.session_state.farms.append({
                "Owner": current_user,
                "Farmer Name": farmer_name,
                "Purok": purok,
                "Farm Name": farm_name,
                "Barangay": barangay,
                "Crop Type": crop_type,
                "Area": area,
                "Planting Start": planting_start.strftime("%Y-%m-%d"),
            })
            st.success(f"🌾 Farm '{farm_name}' registered successfully!")
        else:
            st.error("❌ Please fill all fields.")

# ------------------ USER DASHBOARD ------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.subheader("🌾 My Farm Dashboard")
user_farms = [f for f in st.session_state.farms if f["Owner"] == current_user]

if user_farms:
    df_user_farms = pd.DataFrame(user_farms)
    st.dataframe(df_user_farms, use_container_width=True)

    selected_farm = st.selectbox("Select a farm for AI irrigation recommendation", [f["Farm Name"] for f in user_farms])
    farm = next(f for f in user_farms if f["Farm Name"] == selected_farm)
    soil, temp, humidity, water, weather = get_sensor_data()
    water_need = predict_water_need(weather, soil, farm["Crop Type"])
    recommendation = generate_recommendation(water_need)

    st.markdown("### 💧 AI Irrigation Recommendation")
    st.write(f"*Weather:* {weather}")
    st.write(f"*Soil Moisture:* {soil:.1f}%")
    st.write(f"*Temperature:* {temp:.1f}°C")
    st.write(f"*Humidity:* {humidity:.1f}%")
    st.write(f"*Water Level:* {water:.0f} L")
    st.success(recommendation)

    st.markdown("### 🤖 AI Harvest Analysis")
    with st.form("harvest_form"):
        fertilizer_used = st.selectbox("Fertilizer Type", ["Organic", "Inorganic", "Mixed"])
        irrigation_method = st.selectbox("Irrigation Method", ["Drip", "Sprinkler", "Flood", "Manual"])
        pest_control = st.selectbox("Pest Control Applied?", ["Yes", "No"])
        submit_analysis = st.form_submit_button("🔍 Analyze Harvest")

        if submit_analysis:
            base_yield = {"Rice": 6.0, "Corn": 5.0, "Vegetables": 8.0}[farm["Crop Type"]]
            modifier = 1.0
            if fertilizer_used == "Organic": modifier += 0.1
            elif fertilizer_used == "Inorganic": modifier += 0.05
            if irrigation_method == "Drip": modifier += 0.15
            elif irrigation_method == "Flood": modifier -= 0.05
            if pest_control == "Yes": modifier += 0.1

            estimated_yield = base_yield * modifier * farm["Area"]
            days_to_harvest = random.randint(90, 120)
            quality = random.choice(["Excellent", "Good", "Average", "Below Average"])

            result = {
                "Owner": current_user,
                "Farm Name": farm["Farm Name"],
                "Crop Type": farm["Crop Type"],
                "Fertilizer": fertilizer_used,
                "Irrigation": irrigation_method,
                "Pest Control": pest_control,
                "Estimated Yield (tons)": round(estimated_yield, 2),
                "Days to Harvest": days_to_harvest,
                "Quality": quality
            }
            st.session_state.harvest_results.append(result)

            st.success(f"🌾 *Harvest Prediction for {farm['Farm Name']}*")
            st.write(f"📦 Estimated Yield: *{estimated_yield:.2f} tons*")
            st.write(f"🗓️ Days until Harvest: *{days_to_harvest} days*")
            st.write(f"⭐ Expected Quality: *{quality}*")
else:
    st.info("You haven't registered any farms yet.")
st.markdown('</div>', unsafe_allow_html=True)

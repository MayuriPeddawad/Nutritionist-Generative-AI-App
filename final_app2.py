
import streamlit as st
from PIL import Image
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="NutriGen - Nutrition Calculator & Diet Planner", layout="wide")

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# File to store user data
USER_DATA_FILE = "users.json"

# Initialize session state for login and registration
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'registration_message' not in st.session_state:
    st.session_state.registration_message = ""
if 'password_reset_message' not in st.session_state:
    st.session_state.password_reset_message = ""

# Load user data from file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to file
def save_user_data(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Initialize users in session state from file
if 'users' not in st.session_state:
    st.session_state.users = load_user_data()

# Function to load Google Gemini model and get response for diet planning
def get_response_diet(prompt, input):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  
        response = model.generate_content([prompt, input])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to load Google Gemini model and get response for nutrition analysis
def get_response_nutrition(image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')  
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Preprocess image data
def prep_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded!")


# Main UI
st.title("NutriGen - Your Personalized Nutrition and Diet Planner")


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Nutrition Calculator", "Diet Planner", "Meal Plan", "About", "Contact Us"])

if page == "Home":
    st.header("Welcome to NutriGen!")
    st.write("NutriGen helps you calculate nutrition from an image, plan your diet based on calorie input, and generate meal plans using selected ingredients.")
    st.image("homepage_logo.png", use_column_width=True)
    st.write("Get started by navigating to one of the sections from the sidebar.")

elif page == "Nutrition Calculator":
    st.header("Nutrition Calculator")
    uploaded_file = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Process Image"):
            image_data = prep_image(uploaded_file)
            prompt = """You are an expert nutritionist. As a skilled nutririonist, you are required to analyze the food items in the image and determine the total nutritional value, also provide the details of every food items with calories intake in below format. You may also give just an estimate of its nutritional content if you are not able to guess it correctly, but make sure that the response that you give sounds professional.
            1. Item 1 - number of calories
            2. Item 2 - number of calories
            ......
            ......
            Finally you can also mention whether the food is healthy or not and also mention the percentage split of the ratio of carbohydrates, fats, fibres, sugar and other important nutrients required in our diet"""
            result = get_response_nutrition(image_data, prompt)
            st.write("**Nutritional Information:**")
            st.write(result)

elif page == "Diet Planner":
    st.header("Diet Planner")
    calorie_input = st.number_input("Enter Your Daily Calorie Goal", min_value=1000, max_value=5000, step=100)
    diet_type = st.selectbox("Select Your Diet Type", ["Balanced", "Keto", "Vegan", "Low Carb", "High Protein"])
    if st.button("Generate Diet Plan"):
        prompt = f"Create a {diet_type} diet plan for a daily intake of {calorie_input} calories."
        result = get_response_diet(prompt, "")
        st.write("**Diet Plan:**")
        st.write(result)

elif page == "Meal Plan":
    st.header("Meal Plan")
    ingredients = st.text_area("Enter Ingredients (comma-separated)", "")
    if st.button("Generate Meal Plan"):
        prompt = f"Generate a meal plan using the following ingredients: {ingredients}."
        result = get_response_diet(prompt, "")
        st.write("**Meal Plan:**")
        st.write(result)

elif page == "About":
    st.header("About NutriGen")
    st.write("NutriGen is a web application that helps you analyze nutrition, plan diets, and create meal plans with ease.")

elif page == "Contact Us":
    st.header("Contact Us")
    st.write("For any inquiries, please reach out at awantigiradkar1621@gmail.com or dhanashree.s.kengale@gmail.com or mmpeddawad08@gmail.com or kavya061427@gmail.com or menonshyama96@gmail.com.")

# Footer (can be added in the Home section or as a common footer)
st.sidebar.title("Quick Links")
st.sidebar.markdown("[Privacy Policy](#)")
st.sidebar.markdown("[Terms of Service](#)")
st.sidebar.markdown("[Contact Us](#)")

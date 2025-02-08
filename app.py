import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(page_title="Concrete Strength Predictor", layout="wide")

# Load the trained model
@st.cache_resource
def load_model():
    try:
        with open("RF_model.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error("Model file 'RF_model.pkl' not found. Please ensure the file is in the same directory.")
        st.stop() 

model = load_model()

# Title and App Introduction
st.title("Concrete Compressive Strength Predictor")
st.markdown("""
    Predict the **compressive strength (MPa)** of concrete based on various input parameters.
    """)
st.image("https://tse4.mm.bing.net/th?id=OIP.nBN3S_Qyjs9cKITUjOv7nwHaGK&pid=Api&P=0&h=180", width=100)

# Sidebar for input fields
st.sidebar.header("Input Parameters")

# Sidebar Inputs
cement = st.sidebar.number_input("Cement (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
slag = st.sidebar.number_input("Slag (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
fly_ash = st.sidebar.number_input("Fly Ash (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
water = st.sidebar.number_input("Water (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
superplasticizer = st.sidebar.number_input("Superplasticizer (kg/m³)", min_value=0.0, step=0.1, format="%.2f")
coarse_aggregate = st.sidebar.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
fine_aggregate = st.sidebar.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0, format="%.2f")
age = st.sidebar.number_input("Age (days)", min_value=1, step=1, format="%d")

# Input Feature Visualization (Bar Chart)
st.subheader("Input Feature Visualization")
feature_names = ["Cement", "Slag", "Fly Ash", "Water", "Superplasticizer", "Coarse Aggregate", "Fine Aggregate", "Age (days)"]
feature_values = [cement, slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age]

# Plot a bar chart to visualize the input values
fig, ax = plt.subplots()
ax.barh(feature_names, feature_values, color='skyblue')
ax.set_xlabel("Values")
ax.set_title("Input Feature Values")
st.pyplot(fig)

# Prediction Button
if st.sidebar.button("Predict"):
    try:
        # Prepare the input features for the model
        input_features = np.array([[cement, slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age]])
        
        # Make prediction
        prediction = model.predict(input_features)[0]
        
        # Display the result
        st.subheader("Predicted Concrete Compressive Strength (MPa)")
        st.success(f"Predicted Concrete Compressive Strength: {prediction:.2f} MPa")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Footer with additional info
st.markdown("""
    --- 
    <small>Developed by Tatva Infraprojects.</small>
    <small>© 2024</small>
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Unit Converter", 
    page_icon="🔄", 
    layout="wide"
)

# Custom CSS - simplified but still attractive
st.markdown("""
<style>
    /* Main container styling */
    .main {padding: 0rem 1rem;}
    
    /* Result container styling */
    .result-container {
        background: linear-gradient(135deg, #4158D0, #C850C0);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .header-text {
        font-size: 2rem;
        font-weight: bold;
        color: #4158D0;
        margin-bottom: 10px;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #4158D0;
        color: white;
        border-radius: 8px;
    }
    
    /* Category buttons */
    .category-button {
        margin-right: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []
if 'current_category' not in st.session_state:
    st.session_state.current_category = "Length"

# Category icons
CATEGORY_ICONS = {
    "Length": "📏", "Weight": "⚖️", "Temperature": "🌡️",
    "Area": "📐", "Volume": "🧪", "Time": "⏱️"
}

# Unit conversion dictionaries
UNITS = {
    "Length": {
        "units": ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Yards", "Feet", "Inches"],
        "base": "Meters",
        "conversions": {
            "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01, "Millimeters": 0.001,
            "Miles": 1609.34, "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254
        }
    },
    "Weight": {
        "units": ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces", "Stone"],
        "base": "Kilograms",
        "conversions": {
            "Kilograms": 1, "Grams": 0.001, "Milligrams": 0.000001,
            "Pounds": 0.453592, "Ounces": 0.0283495, "Stone": 6.35029
        }
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "base": None,  # Special case with custom conversion
        "conversions": {}
    },
    "Area": {
        "units": ["Square Meters", "Square Kilometers", "Square Centimeters", "Hectares", "Acres", "Square Miles"],
        "base": "Square Meters",
        "conversions": {
            "Square Meters": 1, "Square Kilometers": 1000000, "Square Centimeters": 0.0001,
            "Hectares": 10000, "Acres": 4046.86, "Square Miles": 2589988.11
        }
    },
    "Volume": {
        "units": ["Liters", "Milliliters", "Cubic Meters", "Gallons (US)", "Fluid Ounces (US)", "Cups"],
        "base": "Liters",
        "conversions": {
            "Liters": 1, "Milliliters": 0.001, "Cubic Meters": 1000,
            "Gallons (US)": 3.78541, "Fluid Ounces (US)": 0.0295735, "Cups": 0.236588
        }
    },
    "Time": {
        "units": ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months (avg)", "Years (avg)"],
        "base": "Seconds",
        "conversions": {
            "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400,
            "Weeks": 604800, "Months (avg)": 2629746, "Years (avg)": 31556952
        }
    }
}

# Function to update history
def add_to_history(category, from_val, from_unit, to_val, to_unit):
    st.session_state.conversion_history.insert(0, {
        "Category": category,
        "Input": f"{from_val} {from_unit}",
        "Output": f"{to_val} {to_unit}",
        "Time": datetime.now().strftime("%H:%M:%S")
    })
    
    # Keep only most recent 10 conversions
    if len(st.session_state.conversion_history) > 10:
        st.session_state.conversion_history = st.session_state.conversion_history[:10]

# App header
st.markdown('<div class="header-text">📊 Enhanced Unit Converter</div>', unsafe_allow_html=True)

# Category selection buttons
st.write("Select Category:")
cols = st.columns(len(UNITS.keys()))
for i, cat in enumerate(UNITS.keys()):
    with cols[i]:
        if st.button(f"{CATEGORY_ICONS.get(cat, '🔄')} {cat}", key=f"cat_{cat}", 
                    help=f"Convert {cat} units"):
            st.session_state.current_category = cat
            st.rerun()

# Current category
category = st.session_state.current_category
st.subheader(f"{CATEGORY_ICONS.get(category, '🔄')} {category} Converter")

# Main conversion interface
col1, col2 = st.columns(2)

with col1:
    input_value = st.number_input("Enter Value:", value=1.0, format="%.6g")
    from_unit = st.selectbox("From:", UNITS[category]["units"])

with col2:
    to_unit = st.selectbox("To:", UNITS[category]["units"])
    
    # Calculate converted value
    if category == "Temperature":
        # Special case for temperature
        if from_unit == to_unit:
            result = input_value
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            result = (input_value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            result = input_value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            result = (input_value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            result = ((input_value - 32) * 5/9) + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            result = input_value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            result = ((input_value - 273.15) * 9/5) + 32
    else:
        # Standard conversion using base unit
        base_unit = UNITS[category]["base"]
        base_value = input_value * UNITS[category]["conversions"][from_unit]
        result = base_value / UNITS[category]["conversions"][to_unit]

# Results display
st.markdown("<div class='result-container'>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: 2rem;'>{input_value} {from_unit} = {result:.6g} {to_unit}</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Add to history button
if st.button("📝 Save to History"):
    add_to_history(category, input_value, from_unit, f"{result:.6g}", to_unit)
    st.success("Conversion added to history!")

# Display visualization for applicable categories
if category in ["Length", "Weight", "Volume", "Area"] and from_unit != to_unit:
    st.subheader("📊 Visual Comparison")
    
    # Create comparison data for visualization
    if input_value > 0:
        # Create scale factor for better visualization
        scale_factor = 1
        if result / input_value > 100:
            scale_factor = 100
        elif result / input_value > 10:
            scale_factor = 10
        elif input_value / result > 100:
            scale_factor = 0.01
        elif input_value / result > 10:
            scale_factor = 0.1
            
        chart_data = pd.DataFrame({
            'Unit': [from_unit, to_unit],
            'Value': [input_value, result],
            'Normalized': [input_value if from_unit == to_unit else input_value * scale_factor, 
                          result if from_unit == to_unit else result * scale_factor]
        })
        
        # Create bar chart
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Unit:N', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Normalized:Q', title='Value (scaled for comparison)'),
            color=alt.Color('Unit:N', scale=alt.Scale(scheme='blues'), legend=None),
            tooltip=['Unit', 'Value']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
        
        if scale_factor != 1:
            st.caption(f"Note: Values are scaled for better visualization comparison")

# Formula explanation
with st.expander("See Conversion Formula"):
    if category == "Temperature":
        st.markdown("#### Temperature Conversion Formulas:")
        if from_unit == to_unit:
            st.markdown(f"No conversion needed")
        elif from_unit == "Celsius" and to_unit == "Fahrenheit":
            st.markdown(f"°F = (°C × 9/5) + 32\n\n{input_value}°C = ({input_value} × 9/5) + 32 = {result:.6g}°F")
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            st.markdown(f"K = °C + 273.15\n\n{input_value}°C = {input_value} + 273.15 = {result:.6g}K")
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            st.markdown(f"°C = (°F - 32) × 5/9\n\n{input_value}°F = ({input_value} - 32) × 5/9 = {result:.6g}°C")
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            st.markdown(f"K = (°F - 32) × 5/9 + 273.15\n\n{input_value}°F = ({input_value} - 32) × 5/9 + 273.15 = {result:.6g}K")
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            st.markdown(f"°C = K - 273.15\n\n{input_value}K = {input_value} - 273.15 = {result:.6g}°C")
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            st.markdown(f"°F = (K - 273.15) × 9/5 + 32\n\n{input_value}K = ({input_value} - 273.15) × 9/5 + 32 = {result:.6g}°F")
    else:
        base_unit = UNITS[category]["base"]
        base_value = input_value * UNITS[category]["conversions"][from_unit]
        st.markdown(f"#### {category} Conversion Formula:")
        st.markdown(f"1. Convert {from_unit} to {base_unit}: {input_value} × {UNITS[category]['conversions'][from_unit]} = {base_value:.6g} {base_unit}")
        st.markdown(f"2. Convert {base_unit} to {to_unit}: {base_value:.6g} ÷ {UNITS[category]['conversions'][to_unit]} = {result:.6g} {to_unit}")

# Quick reference table
with st.expander("Quick Reference Table"):
    if category != "Temperature":
        base_unit = UNITS[category]["base"]
        reference_value = 1.0
        
        # Generate reference data
        ref_data = []
        for unit in UNITS[category]["units"]:
            if category == "Temperature":
                continue  # Skip for temperature due to different conversion
            
            converted = reference_value * UNITS[category]["conversions"][base_unit] / UNITS[category]["conversions"][unit]
            ref_data.append({
                "Unit": unit,
                f"Equivalent to 1 {base_unit}": f"{converted:.6g}"
            })
        
        st.dataframe(pd.DataFrame(ref_data), hide_index=True, use_container_width=True)
    else:
        st.markdown("""
        | From  | To | Formula |
        | ----- | -- | ------- |
        | Celsius | Fahrenheit | °F = (°C × 9/5) + 32 |
        | Celsius | Kelvin | K = °C + 273.15 |
        | Fahrenheit | Celsius | °C = (°F - 32) × 5/9 |
        | Fahrenheit | Kelvin | K = (°F - 32) × 5/9 + 273.15 |
        | Kelvin | Celsius | °C = K - 273.15 |
        | Kelvin | Fahrenheit | °F = (K - 273.15) × 9/5 + 32 |
        """)

# History section
st.header("📜 Recent Conversions")

if 'conversion_history' not in st.session_state or not st.session_state.conversion_history:
    st.info("Your conversion history will appear here.")
else:
    history_df = pd.DataFrame(st.session_state.conversion_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    if st.button("Clear History"):
        st.session_state.conversion_history = []
        st.experimental_rerun()

# Simple footer
st.markdown("---")
st.markdown("📊 Unit Converter | Made by Taha")
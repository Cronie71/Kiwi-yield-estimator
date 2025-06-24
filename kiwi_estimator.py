import streamlit as st

# --- Load from secrets ---

PASSWORD = st.secrets["auth"]["password"]

def login():

    st.title("Login Required")
    password = st.text_input("Enter password:", type="password")

    if password == "":
        st.info("Please enter your password to access the program.")
        st.stop()

    if password != PASSWORD:
        st.error("Incorrect password. Try again.")
        st.stop()

    # ✅ Show disclaimer after successful login

    with st.expander("📘 Disclaimer & Assumptions", expanded=True):
        st.markdown(
            """
            ### 📌 Important Information
            
            This calculator is provided as a general **planning tool** for kiwi fruit yield and revenue estimation until further development.
            
            - Estimates are based on user inputs and standard assumptions.
            - Actual results may vary due to farm-specific factors such as climate, irrigation, fruit set variation, and tree age.
            - **No liability** is accepted by the developer or distributor for financial decisions or crop outcomes influenced by this program.
            
            ---
            ### Yield Standard Assumption
            - This tool assumes a standard planting density of **666 trees per hectare**, based on:
                - 100m rows with 5m row spacing → 20 rows/ha
                - 3m between trees → 33.33 trees/row
                - → **~666 trees/ha**
            """
        )

    # ✅ Add confirm checkbox before continuing

    if not st.checkbox("I have read and accept the information above."):
        st.warning("You must acknowledge the disclaimer to continue.")
        st.stop()

login()

st.title("Kiwi Fruit Production Estimator")

# Constants
canes_per_plant = 16

# Choose mode
option = st.radio(
    "What do you want to estimate?",
    [
        "Flowers per Cane to Hit Target Yield",
        "Revenue Estimate"
    ]
)

if option == "Flowers per Cane to Hit Target Yield":

    st.header("Estimate Flowers per Cane Needed")

    # Inputs
    num_trees = st.number_input("Number of trees on your farm:", min_value=1, value=666)
    land_size = st.number_input("Land size (hectares):", min_value=0.1, value=1.0)
    target_yield_ton_per_hectare = st.number_input("Target yield per hectare (tons):", min_value=1.0, value=10.0)
    fruit_weight = st.number_input("Average fruit weight (grams):", min_value=1.0, value=90.0)

    if st.button("Calculate Flowers per Cane"):

        target_kg = target_yield_ton_per_hectare * 1000 * land_size
        total_canes = num_trees * canes_per_plant
        fpc = target_kg / (total_canes * fruit_weight)

        st.success(f"To reach your target of {target_yield_ton_per_hectare:.1f} tons/ha,")
        st.success(f"You need to leave **{fpc:.2f} flowers per cane**.")

elif option == "Revenue Estimate":

    st.header("Estimate Revenue")

    # Inputs
    num_trees = st.number_input("Number of trees on your farm:", min_value=1, value=666)
    fpc = st.number_input("Flowers per cane:", min_value=0.0, value=8.0, step=0.1)
    avg_price = st.number_input("Average fruit price per kg (ZAR):", min_value=0.0, value=60.0)
    fruit_weight = st.number_input("Average fruit weight (grams):", min_value=1.0, value=90.0)

    if st.button("Estimate Revenue"):

        total_canes = num_trees * canes_per_plant
        total_kg = fpc * total_canes * fruit_weight / 1000  # convert grams to kg
        revenue = total_kg * avg_price
        revenue_per_tree = revenue / num_trees

        st.success(f"Estimated Yield: **{total_kg:,.2f} kg**")
        st.success(f"Total Revenue: **R{revenue:,.2f}**")
        st.info(f"Revenue per Tree: **R{revenue_per_tree:.2f}**")

st.markdown(
    """
    <style>
    /* Universal link styling override */
    a:link, a:visited, a:hover, a:active, a:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
        background: none !important;
        color: #cc6600 !important;  /* Match your theme */
        text-decoration: none !important;
    }

    /* Remove persistent focus indicators from all elements */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Optional: Fixes Streamlit-specific components */
    section:focus-within {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Optional: Input border fix */
    input:focus, textarea:focus {
        border: 1px solid #0f0 !important;
        box-shadow: none !important;
    }
    </style>

    <a href="https://buymeacoffee.com/jacques05" target="_blank" style="
        display:inline-block;
        padding:10px 15px;
        background-color:#fff3e0;
        color:#cc6600;
        font-weight:bold;
        border-radius:8px;
        text-decoration:none;
        border: 2px solid #cc6600;
        ">
        Support this program
    </a>
    """,
    unsafe_allow_html=True
)

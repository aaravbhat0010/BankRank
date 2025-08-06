import streamlit as st
import altair as alt
from utils.recommender import recommend_banks

st.set_page_config(page_title="BankRank", layout="centered")

st.title("🏦 BankRank")
st.write("Find the best savings or checking account based on your preferences — from student accounts to elite private banking.")

# --- Sidebar filters with HIGH LIMITS for premium accounts ---
st.sidebar.header("Your Preferences")
min_apy = st.sidebar.slider("Minimum APY (%)", 0.0, 100.0, 1.0, step=0.1)
max_fee = st.sidebar.slider("Max Monthly Fee ($)", 0, 5000, 10)

student = st.sidebar.checkbox("Student Friendly")

preferences = {
    "min_apy": min_apy,
    "max_fee": max_fee,
    "student_friendly": student
}

# --- Button to trigger recommendation ---
if st.button("Find My Bank"):
    ranked_banks = recommend_banks(preferences)

    if not ranked_banks.empty:
        top_bank = ranked_banks.iloc[0]
        worst_bank = ranked_banks.iloc[-1]
        savings = worst_bank["Monthly Fee"] - top_bank["Monthly Fee"]

        st.success("🏆 Your Top Match")
        st.markdown(f"""
        **{top_bank['Bank']}** — *{top_bank['Account Type']}*

        - **APY:** {top_bank['APY']}%
        - **Monthly Fee:** ${top_bank['Monthly Fee']}
        - **Mobile Rating:** {top_bank['Mobile Rating']} ⭐
        - ✅ **No ATM Fees:** {"Yes" if top_bank["No ATM Fees"] == "Yes" else "❌ No"}
        - 📱 **Mobile App:** {"Available" if top_bank["Mobile App"] == "Yes" else "Unavailable"}
        """)

        if savings > 0:
            st.info(f"💸 By choosing **{top_bank['Bank']}** over **{worst_bank['Bank']}**, you save **${savings:.2f} per month** in fees.")

        st.divider()

        st.subheader("📈 Visual Comparison")

        top_n = ranked_banks.head(5)

        st.markdown("### APY by Bank (Top 5)")
        apy_chart = alt.Chart(top_n).mark_bar().encode(
            x=alt.X("Bank", sort="-y"),
            y="APY",
            color=alt.value("#4CAF50"),
            tooltip=["Bank", "APY"]
        ).properties(width=600)
        st.altair_chart(apy_chart)

        st.markdown("### Monthly Fee by Bank (Top 5)")
        fee_chart = alt.Chart(top_n).mark_bar().encode(
            x=alt.X("Bank", sort="-y"),
            y="Monthly Fee",
            color=alt.value("#F44336"),
            tooltip=["Bank", "Monthly Fee"]
        ).properties(width=600)
        st.altair_chart(fee_chart)

        st.divider()
        st.subheader("🔍 All Matches")
        st.dataframe(ranked_banks)

    else:
        st.warning("No banks match your criteria.")

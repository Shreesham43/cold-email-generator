import streamlit as st
from chain import Chain
from porfolio import Portfolio

def create_streamlit_app():
    st.title("Email Generator")
    job_url = st.text_input("Enter job url")
    submit = st.button("Generate Email")
    if submit:
        try:
            chain = Chain()
            parsed_job = chain.extract_job(job_url)
            portfolio = Portfolio()
            portfolio.load_portfolios()
            links = portfolio.get_portfolio_links(parsed_job[0]["skills_required"])
            email = chain.generate_email(parsed_job[0], links)
            st.write(email)
        except Exception as e:
            st.write(f"Error: {e}")

if __name__ == "__main__":
    create_streamlit_app()
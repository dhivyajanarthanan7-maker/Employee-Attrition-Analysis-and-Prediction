import streamlit as st
import pandas as pd
import pickle
with open('rfc2.score.pkl', 'rb') as f:
    model = pickle.load(f)

st.set_page_config(page_title="Employee Attrition Analysis", page_icon=":bar_chart:", layout="wide")    
st.sidebar.title("Employee Attrition Prediction")
menu=st.sidebar.radio("Navigate", ["Dashboard Home", "Predict Employee Attrition"])
if menu=="Dashboard Home":
    st.markdown("<h2 style='text-align: center; color: black;'>Employee Attrition Analysis Dashboard</h2>", unsafe_allow_html=True)
    st.info("View high-risk employees and key insights to reduce attrition rates.")
    df = pd.read_csv(r'C:\Users\user\Desktop\CapstoneProject\Employee_Attrition\filtered_dataset.csv')
    st.dataframe(df)
    st.subheader("Key Insights")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", len(df))
    col2.metric("Average Engagement Score", round(df['EngagementScore'].mean(), 2))
    col3.metric("Attrition Rate", f"{round(df['Attrition'].mean()*100, 2)}%")
elif menu=="Predict Employee Attrition":
    st.markdown("<h2 style='text-align: center; color: black;'>Predict Employee Attrition</h2>", unsafe_allow_html=True)
    st.write("Enter the employee details below to predict the  of attrition.")
    with st.form(key='attrition_form'):
        col1, col2 = st.columns(2)
        with col1:
            PerformanceToSalary = st.number_input("Performance to Salary Ratio", min_value=0.0, max_value=10.0, step=0.1)
            MonthlyIncome = st.number_input("Monthly Income", min_value=1000, max_value=20000, step=100)
            EngagementScore = st.number_input("Engagement Score", min_value=0.0, max_value=10.0, step=0.1)
            Age = st.number_input("Age", min_value=18, max_value=60, step=1)
            OverTime = st.selectbox("OverTime (1 = Yes, 0 = No)", [0, 1])
            DistanceFromHome = st.number_input("Distance From Home", min_value=0, max_value=30, step=1)
            ExperiencePerformance = st.number_input("Experience Performance", min_value=0, max_value=10, step=1)
            TotalWorkingYears = st.number_input("Total Working Years", min_value=0, max_value=40, step=1)
        with col2:
            YearsAtCompany = st.number_input("Years at Company", min_value=0, max_value=40, step=1)
            NumCompaniesWorked = st.number_input("Number of Companies Worked", min_value=0, max_value=10, step=1)
            PercentSalaryHike = st.number_input("Percent Salary Hike", min_value=0, max_value=100, step=1)
            PromotionGapRatio = st.number_input("Promotion Gap Ratio", min_value=0.0, max_value=10.0, step=0.1)
            JobRole = st.number_input("Job Role (encoded)", min_value=0, max_value=10, step=1)
            StockOptionLevel = st.number_input("Stock Option Level", min_value=0, max_value=3, step=1)
            YearsWithCurrManager = st.number_input("Years With Current Manager", min_value=0.0, max_value=20.0, step=0.5)
        submit_button = st.form_submit_button(label='Predict Attrition')
    if submit_button:
        input_data = pd.DataFrame({
            'PerformanceToSalary': [PerformanceToSalary],
            'MonthlyIncome': [MonthlyIncome],
            'EngagementScore': [EngagementScore],
            'Age': [Age],
            'OverTime': [OverTime],
            'DistanceFromHome': [DistanceFromHome],
            'ExperiencePerformance': [ExperiencePerformance],
            'TotalWorkingYears': [TotalWorkingYears],
            'YearsAtCompany': [YearsAtCompany],
            'NumCompaniesWorked': [NumCompaniesWorked],
            'PercentSalaryHike': [PercentSalaryHike],
            'PromotionGapRatio': [PromotionGapRatio],
            'JobRole': [JobRole],
            'StockOptionLevel': [StockOptionLevel],
            'YearsWithCurrManager': [YearsWithCurrManager]},
             columns=['PerformanceToSalary', 'MonthlyIncome', 'EngagementScore', 'Age', 'OverTime', 'DistanceFromHome', 
                      'ExperiencePerformance', 'TotalWorkingYears', 'YearsAtCompany', 'NumCompaniesWorked', 
                      'PercentSalaryHike', 'PromotionGapRatio', 'JobRole', 'StockOptionLevel', 'YearsWithCurrManager'])
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]*100
        if prediction[0] == 1:
            st.error("The employee is likely to leave the company.")
        else:
            st.success("The employee is likely to stay with the company.")

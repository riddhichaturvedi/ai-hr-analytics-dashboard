# AI HR Analytics Dashboard

## Overview

This project is an interactive HR analytics dashboard designed to transform raw employee data into meaningful business insights. It helps HR teams analyze workforce trends, monitor attrition patterns, and understand key factors affecting employee retention.

The application is built using Streamlit and provides an intuitive interface for exploring HR metrics, visualizations, and rule-based risk analysis.

---

## Live Application

https://ai-hr-analytics-dashboard-svb68uox7s324flrnfddbf.streamlit.app/

---

## Problem Statement

Employee attrition is a major challenge for organizations, leading to increased hiring costs and loss of talent. Traditional HR reporting systems are often static and lack predictive capabilities.

This project aims to address these limitations by providing:
- Interactive workforce analytics
- Real-time visual insights
- Early identification of attrition risk factors

---

## Key Features

### Workforce Analytics
- Total employee count
- Attrition rate analysis
- Average salary and job satisfaction metrics

### Department and Demographic Analysis
- Attrition distribution by department
- Gender diversity breakdown
- Employee tenure trends

### Salary and Satisfaction Insights
- Salary distribution visualization
- Job satisfaction trends across employees

### Attrition Risk Analysis
- Rule-based risk scoring system
- Classification of employees into High Risk and Low Risk categories
- Risk factors include:
  - Job satisfaction
  - Work-life balance
  - Overtime status

### Data Export
- Ability to download processed dataset as CSV

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---

## Project Structure
ai-hr-analytics-dashboard/
│
├── app.py Main Streamlit application
├── hr_data.csv Dataset used for analysis
├── requirements.txt Project dependencies
├── README.md Project documentation


---

## How to Run Locally

1. Clone the repository
git clone https://github.com/riddhichaturvedi/ai-hr-analytics-dashboard.git


2. Navigate to the project directory
cd ai-hr-analytics-dashboard


3. Install dependencies
pip install -r requirements.txt


4. Run the application
streamlit run app.py


---

## Business Impact

This dashboard helps organizations:
- Identify high attrition risk areas
- Understand workforce behavior patterns
- Improve employee retention strategies
- Support data-driven HR decision making

---

## Future Improvements

- Machine learning-based attrition prediction model
- Integration with real-time HR databases
- Advanced analytics using predictive modeling
- Automated reporting system for HR teams

---

## Author

Riddhi Chaturvedi  
B.Tech Computer Science  
Focus: Data Analytics and AI in HR Systems
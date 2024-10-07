import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config (this must be the first Streamlit command)
st.set_page_config(page_title="GitHub Projects Dashboard", layout="wide")

# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv('github_dataset.csv')
    return df

# Title
st.title("GitHub Projects Dashboard")

# Load data
df = load_data()

# Sidebar
st.sidebar.header("Filters")
language_filter = st.sidebar.multiselect(
    "Select Language", 
    options=df['language'].dropna().unique(),
    default=df['language'].dropna().unique()[:3].tolist()
)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Languages")
    top_languages = df['language'].value_counts().head(10)
    fig_languages = px.bar(top_languages, x=top_languages.index, y=top_languages.values)
    fig_languages.update_layout(xaxis_title="Language", yaxis_title="Number of Projects")
    st.plotly_chart(fig_languages)

with col2:
    st.subheader("Stars vs. Forks")
    fig_scatter = px.scatter(df[df['language'].isin(language_filter)], 
                             x="forks_count", y="stars_count", 
                             color="language", hover_name="repositories",
                             log_x=True, log_y=True)
    fig_scatter.update_layout(xaxis_title="Forks (log scale)", yaxis_title="Stars (log scale)")
    st.plotly_chart(fig_scatter)

st.subheader("Issues vs. Pull Requests")
fig_issues_prs = px.scatter(df[df['language'].isin(language_filter)], 
                            x="issues_count", y="pull_requests", 
                            color="language", hover_name="repositories",
                            size="stars_count", size_max=50)
fig_issues_prs.update_layout(xaxis_title="Issues Count", yaxis_title="Pull Requests Count")
st.plotly_chart(fig_issues_prs)

st.subheader("Contributors Distribution")
fig_contributors = px.box(df[df['language'].isin(language_filter)], x="language", y="contributors", 
                          points="all", hover_name="repositories")
fig_contributors.update_layout(xaxis_title="Language", yaxis_title="Number of Contributors")
st.plotly_chart(fig_contributors)

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Projects", len(df))
col2.metric("Total Languages", df['language'].nunique())
col3.metric("Avg Stars", round(df['stars_count'].mean(), 2))
col4.metric("Avg Forks", round(df['forks_count'].mean(), 2))

# Data Table
st.subheader("Project Details")
st.dataframe(df)

# Additional Insights
st.subheader("Additional Insights")

# Correlation Heatmap
st.write("Correlation between numeric variables:")
numeric_cols = ['stars_count', 'forks_count', 'issues_count', 'pull_requests', 'contributors']
corr = df[numeric_cols].corr()
fig_corr = px.imshow(corr, text_auto=True, aspect="auto")
st.plotly_chart(fig_corr)

# Top Projects
st.write("Top 10 Projects by Stars:")
top_projects = df.nlargest(10, 'stars_count')[['repositories', 'language', 'stars_count', 'forks_count']]
st.table(top_projects)

# Language Statistics
st.write("Language Statistics:")
lang_stats = df.groupby('language').agg({
    'stars_count': 'mean',
    'forks_count': 'mean',
    'issues_count': 'mean',
    'pull_requests': 'mean',
    'contributors': 'mean'
}).round(2)
st.dataframe(lang_stats)

# Data Quality Check
st.subheader("Data Quality Check")
missing_data = df.isnull().sum()
if missing_data.sum() > 0:
    st.write("Missing values in the dataset:")
    st.write(missing_data[missing_data > 0])
else:
    st.write("No missing values found in the dataset.")

# Potential Outliers
st.write("Potential outliers (values above 99th percentile):")
for col in numeric_cols:
    threshold = df[col].quantile(0.99)
    outliers = df[df[col] > threshold]
    if not outliers.empty:
        st.write(f"{col}: {len(outliers)} potential outliers (>{threshold:.2f})")

# Add your insights
st.subheader("Insights and Observations")
st.text_area("Enter your insights here:", 
             "Based on the data, we can observe that...\n"
             "1. ...\n"
             "2. ...\n"
             "3. ...")
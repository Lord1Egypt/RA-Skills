# Streamlit API Quick Reference

Quick reference for commonly used Streamlit functions.

## Page Configuration

```python
st.set_page_config(
    page_title="App Title",
    page_icon="📊",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

## Text Elements

```python
st.title("Title")
st.header("Header")
st.subheader("Subheader")
st.text("Fixed width text")
st.markdown("**Bold** and *italic*")
st.caption("Small caption")
st.code("code block", language="python")
st.latex(r"\int_a^b f(x)dx")
```

## Data Display

```python
st.dataframe(df)  # Interactive
st.table(df)  # Static
st.json({"key": "value"})
st.metric("Label", value=123, delta=10)
```

## Input Widgets

```python
# Text
st.text_input("Label", value="default")
st.text_area("Label", height=100)
st.number_input("Label", min_value=0, max_value=100, value=50)

# Selection
st.selectbox("Label", ["Option 1", "Option 2"])
st.multiselect("Label", ["A", "B", "C"])
st.radio("Label", ["Yes", "No"])
st.slider("Label", 0, 100, 50)
st.select_slider("Label", options=[1, 2, 3, 4, 5])

# Boolean
st.checkbox("Label")
st.toggle("Label")

# Buttons
st.button("Click me")
st.download_button("Download", data, "file.txt")
st.link_button("Go to URL", "https://example.com")

# Date/Time
st.date_input("Select date")
st.time_input("Select time")

# File
st.file_uploader("Choose file", type=['csv', 'xlsx'])
st.camera_input("Take photo")

# Color
st.color_picker("Pick color")
```

## Charts

```python
# Native charts
st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)
st.scatter_chart(df)

# Map
st.map(df)  # df must have 'lat' and 'lon' columns

# External libraries
st.pyplot(fig)  # Matplotlib
st.plotly_chart(fig)  # Plotly
st.altair_chart(chart)  # Altair
st.bokeh_chart(plot)  # Bokeh
```

## Layout

```python
# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Tab 1 content")

# Expander
with st.expander("Click to expand"):
    st.write("Hidden content")

# Container
with st.container():
    st.write("Container content")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.button("Button")
```

## Status & Progress

```python
st.success("Success message")
st.info("Info message")
st.warning("Warning message")
st.error("Error message")
st.exception(Exception("Error details"))

st.progress(0.5)  # 0.0 to 1.0
st.spinner("Loading...")
st.balloons()
st.snow()
```

## Session State

```python
# Initialize
if 'key' not in st.session_state:
    st.session_state.key = 'value'

# Access
st.session_state.key

# Update
st.session_state.key = 'new value'

# Widget with key
st.text_input("Label", key="my_input")
value = st.session_state.my_input
```

## Caching

```python
# Cache data (for dataframes, lists, etc.)
@st.cache_data
def load_data():
    return pd.read_csv('file.csv')

# Cache resources (for models, connections)
@st.cache_resource
def load_model():
    return load_my_model()

# Clear cache
st.cache_data.clear()
st.cache_resource.clear()
```

## Forms

```python
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(f"Name: {name}, Age: {age}")
```

## Media

```python
st.image("image.jpg", caption="Caption")
st.audio("audio.mp3")
st.video("video.mp4")
```

## Control Flow

```python
# Stop execution
st.stop()

# Rerun app
st.rerun()

# Empty placeholder
placeholder = st.empty()
placeholder.text("Text")
placeholder.empty()  # Clear it
```

## Multi-Page Apps

File structure:
```
app.py
pages/
  1_📊_Page1.py
  2_📈_Page2.py
```

In pages:
```python
import streamlit as st

st.title("Page 1")
st.write("Content")
```

## Useful Patterns

### Loading State
```python
with st.spinner("Processing..."):
    result = expensive_operation()
st.success("Done!")
```

### Conditional Display
```python
if st.checkbox("Show details"):
    st.write("Detailed information")
```

### Dynamic Updates
```python
placeholder = st.empty()
for i in range(100):
    placeholder.metric("Progress", i)
    time.sleep(0.1)
```

### File Download
```python
df = pd.DataFrame(data)
csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "data.csv", "text/csv")
```

## Additional Resources

- Full API: https://docs.streamlit.io/develop/api-reference
- Cheat sheet: https://cheat-sheet.streamlit.app/

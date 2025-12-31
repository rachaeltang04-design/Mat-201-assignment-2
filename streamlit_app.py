import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gradient Visualizer", layout="wide")

st.title("Calculus MAT201: Gradient & Direction of Steepest Ascent")
st.markdown("""
This application visualizes **Topic 4: Gradient and Direction of Steepest Ascent**[cite: 8]. 
It calculates the gradient vector $\\nabla f(x,y) = \\langle f_x, f_y \\rangle$ to show the direction of maximum increase[cite: 8].
""")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Select Complexity")
func_option = st.sidebar.radio(
    "Choose Function Type:",
    ("Simple (Paraboloid)", "Complex (Sinusoidal)")
)

st.sidebar.header("2. Select Point $(x_0, y_0)$")
# sliders set to larger range of 5.0
x0 = st.sidebar.slider("x coordinate", -5.0, 5.0, 1.0, step=0.1)
y0 = st.sidebar.slider("y coordinate", -5.0, 5.0, 1.0, step=0.1)

# --- FUNCTION DEFINITIONS ---
if func_option == "Simple (Paraboloid)":
    def f(x, y): return x**2 + y**2
    def df_dx(x, y): return 2*x
    def df_dy(x, y): return 2*y
    equation_latex = r"f(x, y) = x^2 + y^2"
else:
    def f(x, y): return np.sin(x) * np.cos(y)
    def df_dx(x, y): return np.cos(x) * np.cos(y)
    def df_dy(x, y): return -np.sin(x) * np.sin(y)
    equation_latex = r"f(x, y) = \sin(x)\cos(y)"

# --- CALCULATIONS ---
z0 = f(x0, y0)
grad_x = df_dx(x0, y0)
grad_y = df_dy(x0, y0)
magnitude = np.sqrt(grad_x**2 + grad_y**2)

# --- VISUALIZATION MESH ---
x_range = np.linspace(-6, 6, 80)
y_range = np.linspace(-6, 6, 80)
X, Y = np.meshgrid(x_range, y_range)
Z = f(X, Y)

fig = go.Figure()
fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8))

# Add the specific point (Red Dot)
fig.add_trace(go.Scatter3d(x=[x0], y=[y0], z=[z0], mode='markers', marker=dict(size=6, color='red')))

# Add Gradient Vector (Cone)
fig.add_trace(go.Cone(
    x=[x0], y=[y0], z=[z0],
    u=[grad_x], v=[grad_y], w=[magnitude * 0.5], 
    sizemode="absolute", sizeref=1.0, anchor="tail",
    colorscale=[[0, 'red'], [1, 'red']], showscale=False
))

# --- DISPLAY OUTPUTS ---
col1, col2 = st.columns([1, 2])
with col1:
    st.info("Mathematical Details")
    st.latex(r"\text{Function: } " + equation_latex)
    st.latex(r"\text{Point: } P(" + str(x0) + ", " + str(y0) + ")")
    st.write("---")
    st.write("**Partial Derivatives:**")
    st.latex(r"f_x = " + f"{grad_x:.3f}")
    st.latex(r"f_y = " + f"{grad_y:.3f}")
    st.write("---")
    st.write("**Gradient Vector:**")
    st.latex(r"\nabla f = \langle " + f"{grad_x:.3f}, {grad_y:.3f}" + r" \rangle")
    st.success(f"Steepest Ascent Direction: <{grad_x:.2f}, {grad_y:.2f}>")

with col2:
    st.plotly_chart(fig, use_container_width=True)

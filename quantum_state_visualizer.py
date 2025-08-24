import streamlit as st
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, partial_trace, DensityMatrix
import plotly.graph_objects as go
def plot_bloch_plotly(bloch_vector, title="Bloch Sphere"):
    fig = go.Figure()
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    fig.add_surface(x=x, y=y, z=z, opacity=0.15, colorscale="Blues")
    fig.add_trace(go.Scatter3d(x=[0,1], y=[0,0], z=[0,0], mode='lines', line=dict(color='black', width=3)))
    fig.add_trace(go.Scatter3d(x=[0,0], y=[0,1], z=[0,0], mode='lines', line=dict(color='black', width=3)))
    fig.add_trace(go.Scatter3d(x=[0,0], y=[0,0], z=[0,1], mode='lines', line=dict(color='black', width=3)))
    fig.add_trace(go.Scatter3d(
        x=[0, bloch_vector[0]],
        y=[0, bloch_vector[1]],
        z=[0, bloch_vector[2]],
        mode="lines+markers",
        line=dict(color="red", width=6),
        marker=dict(size=6)
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1, 1], title='X'),
            yaxis=dict(range=[-1, 1], title='Y'),
            zaxis=dict(range=[-1, 1], title='Z'),
            aspectmode='cube'
        ),
        title=title,
        margin=dict(l=0, r=0, b=0, t=30)
    )
    return fig
def density_matrix_to_bloch(dm):
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    bloch_x = np.real(np.trace(dm @ X))
    bloch_y = np.real(np.trace(dm @ Y))
    bloch_z = np.real(np.trace(dm @ Z))
    return [bloch_x, bloch_y, bloch_z]
st.set_page_config(page_title="Quantum State Visualizer", layout="wide")
st.title("Quantum State Visualizer (Stateathon Edition)")
st.markdown("Visualize **each qubit's state** on the Bloch sphere from any quantum circuit.")
num_qubits = st.slider("Number of Qubits", 1, 4, 2)
qc = QuantumCircuit(num_qubits)
st.sidebar.header("Quantum Gates")
if st.sidebar.button("Hadamard on Qubit 0"):
    qc.h(0)
if st.sidebar.button("CNOT (0 → 1)"):
    if num_qubits >= 2:
        qc.cx(0, 1)
if st.sidebar.button("RX on Qubit 0 (π/3)"):
    qc.rx(np.pi/3, 0)
if st.sidebar.button("RY on Qubit 1 (π/4)"):
    if num_qubits >= 2:
        qc.ry(np.pi/4, 1)
st.subheader("Quantum Circuit")
st.text(qc.draw())
state = Statevector.from_instruction(qc)
rho_full = DensityMatrix(state)
cols = st.columns(num_qubits)
for i in range(num_qubits):
    trace_out = [j for j in range(num_qubits) if j != i]
    rho_qubit = partial_trace(rho_full, trace_out)
    bloch_vec = density_matrix_to_bloch(rho_qubit)
    cols[i].plotly_chart(plot_bloch_plotly(bloch_vec, f"Qubit {i}"), use_container_width=True)
st.success("Visualization complete! Add more gates to see live updates.")

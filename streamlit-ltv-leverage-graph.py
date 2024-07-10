import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def calculate_effective_ltv(leverage):
    return 1 - (1 / leverage)

def calculate_leverage(effective_ltv):
    return 1 / (1 - effective_ltv)

def calculate_effective_ltv_from_weights(supply_weight, borrow_weight):
    return supply_weight * borrow_weight

def create_chart(current_leverage, current_ltv):
    leverages = np.linspace(1, 11, 100)
    effective_ltvs = [calculate_effective_ltv(lev) for lev in leverages]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=leverages, y=effective_ltvs, mode='lines', name='Effective LTV'))
    fig.add_trace(go.Scatter(x=[current_leverage], y=[current_ltv], mode='markers', marker=dict(size=10, color='red'), name='Current Point'))

    fig.update_layout(
        xaxis_title='Leverage',
        yaxis_title='Effective LTV',
        yaxis_tickformat='.0%',
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            ticktext=['1x', '2x', '3x', '4x', '5x', '6x', '7x', '8x', '9x', '10x', '11x']
        )
    )
    return fig

st.title('Interactive Effective LTV vs Leverage Graph')
st.markdown(f'''
```python
supplyLTV = 50%  # Bonk supply weight
borrowLTV = 100%  # USCD borrow LTV
effectiveLTV = supplyLTV of borrowLTV
maxLeverage = 1 / (1 - effectiveLTV)
```
''')

tab1, tab2, tab3 = st.tabs(["Adjust Effective LTV", "Adjust Leverage", "Calculate from Weights"])

with tab1:
    st.header("1. Adjust Effective LTV to get Leverage")
    effective_ltv_input = st.slider('Effective LTV', min_value=0.0, max_value=0.99, value=0.5, step=0.01, key='ltv_slider')
    leverage_calculated = calculate_leverage(effective_ltv_input)
    st.write(f'Effective LTV: {effective_ltv_input:.2%}')
    st.write(f'Leverage: {leverage_calculated:.2f}x')
    
    chart = create_chart(leverage_calculated, effective_ltv_input)
    st.plotly_chart(chart, use_container_width=True)

with tab2:
    st.header("2. Adjust Leverage to get Effective LTV")
    leverage = st.slider('Leverage', min_value=1.0, max_value=11.0, value=2.0, step=0.1, key='leverage_slider')
    effective_ltv = calculate_effective_ltv(leverage)
    st.write(f'Leverage: {leverage:.2f}x')
    st.write(f'Effective LTV: {effective_ltv:.2%}')
    
    chart = create_chart(leverage, effective_ltv)
    st.plotly_chart(chart, use_container_width=True)

with tab3:
    st.header("3. Calculate from Supply and Borrow Weights")
    supply_weight = st.slider('Supply Weight', min_value=0.0, max_value=1.0, value=0.5, step=0.01, key='supply_slider')
    borrow_weight = st.slider('Borrow Weight', min_value=0.0, max_value=1.0, value=1.0, step=0.01, key='borrow_slider')
    effective_ltv_calculated = calculate_effective_ltv_from_weights(supply_weight, borrow_weight)
    leverage_from_weights = calculate_leverage(effective_ltv_calculated)
    st.write(f'Effective LTV: {effective_ltv_calculated:.2%}')
    st.write(f'Leverage: {leverage_from_weights:.2f}x')
    
    chart = create_chart(leverage_from_weights, effective_ltv_calculated)
    st.plotly_chart(chart, use_container_width=True)

# Explanation
st.markdown("""
## Explanation

This interactive tool allows you to explore the relationship between Leverage and Effective LTV (Loan-to-Value ratio) in three different ways:

1. **Adjust Effective LTV**: Set the desired Effective LTV and see the required leverage.
2. **Adjust Leverage**: Directly change the leverage and see the resulting Effective LTV.
3. **Calculate from Weights**: Input supply and borrow weights to calculate the Effective LTV and corresponding leverage.

The chart consistently shows:
- X-axis: Leverage (displayed as 1x, 2x, 3x, etc.)
- Y-axis: Effective LTV (as a percentage)

The blue line represents the relationship between Leverage and Effective LTV. The red dot shows the current point based on your inputs.

The relationship is governed by these formulas:
- Effective LTV = 1 - (1 / Leverage)
- Leverage = 1 / (1 - Effective LTV)
- Effective LTV = Supply Weight * Borrow Weight

Key points:
1. As Leverage increases, Effective LTV increases but at a decreasing rate.
2. Effective LTV can never reach 100%, but it gets closer as Leverage increases.
3. At Leverage = 1x, Effective LTV is 0%.
4. At Leverage = 2x, Effective LTV is 50%.
5. Higher Leverage values result in higher Effective LTV, indicating increased risk.

Experiment with the sliders in each tab to see how changes affect the position of the red dot on the chart.
""")
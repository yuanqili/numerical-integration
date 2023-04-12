import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

st.title('Numerical Integration Methods')

st.sidebar.header('Rectangular Rule')
alpha = st.sidebar.number_input('Integration lower bound ($\\alpha$)', value=-2.0, step=0.1)
beta = st.sidebar.number_input('Integration upper bound ($\\beta$)', value=2.0, step=0.1)
n = st.sidebar.number_input('Number of subintervals ($n$)', min_value=1, max_value=200, value=10, step=1)
side = st.sidebar.radio('Rectangular side', ['Left', 'Right', 'Midpoint'], horizontal=True)
show_area = st.sidebar.checkbox('Show area of each subinterval', True)
color = st.sidebar.color_picker('Subinterval color', value='#0000ff')

st.sidebar.header('Normal Curve')
mu = st.sidebar.number_input('Mean ($\mu$)', value=0.0, step=0.1)
sigma = st.sidebar.number_input('Standard deviation ($\sigma$)', value=1.0, step=0.1)
xlim_min = st.sidebar.number_input('$x$-axis lower bound', value=-3.0, step=0.1)
xlim_max = st.sidebar.number_input('$x$-axis upper bound', value=3.0, step=0.1)

# st.markdown(r'''
# $$
#     \int_{\alpha}^{\beta} \phi(x) \,\mathrm{d}x
# $$
# '''.replace('##LOWER##', str(alpha)).replace('##UPPER##', str(beta)).replace('##N##', str(n)))

# metrics
metrics = st.columns(2)

fig, axes = plt.subplots(figsize=(12, 4))

# the normal curve
xs = np.linspace(xlim_min, xlim_max, 100)
normal_ys = stats.norm.pdf(xs, mu, sigma)
ylim_max = normal_ys.max() + 0.02
axes.plot(xs, normal_ys, label='Normal(0, 1)')

# regions
divide_xs = np.linspace(alpha, beta, n + 1)
areas = []
width = divide_xs[1] - divide_xs[0]
for a, b in zip(divide_xs[:-1], divide_xs[1:]):
    midpoint = (a + b) / 2
    fa = stats.norm.pdf(a, mu, sigma)
    fb = stats.norm.pdf(b, mu, sigma)
    fm = stats.norm.pdf(midpoint, mu, sigma)

    match side:
        case 'Left':
            height = fa
            area = width * fa
        case 'Right':
            height = fb
            area = width * fb
        case 'Midpoint':
            height = fm
            area = width * fm

    axes.plot([a, b], [height, height], color=color, lw=0.5)
    axes.fill_between([a, b], [0, 0], [height, height], color=color, alpha=0.2)
    areas.append({'a': a, 'b': b, 'width': width, 'height': height, 'area': area})
    if show_area:
        axes.text(midpoint, 0.02, f'{area:.2f}', ha='center', va='bottom', fontsize=10,
                  bbox=dict(boxstyle='round', facecolor='white', edgecolor=color, alpha=0.8))

# configurations
axes.grid(ls='-', lw=0.5, alpha=0.2, zorder=0)
axes.set_xlim(xlim_min, xlim_max)
axes.set_ylim(0, ylim_max)

st.pyplot(fig)
st.dataframe(pd.DataFrame(areas), use_container_width=True)

area = sum([a['area'] for a in areas])
actual_area = stats.norm.cdf(beta, mu, sigma) - stats.norm.cdf(alpha, mu, sigma)
error = (area - actual_area) / actual_area * 100
with metrics[0]:
    st.metric('Actual Area', f'{actual_area:.8f}')
with metrics[1]:
    st.metric('Numerical Integration Area', f'{area:.8f}', f'{error:.8f}%')

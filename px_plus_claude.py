# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:32:53 2026

@author: berze
"""

# -*- coding: utf-8 -*-
"""
Flyaway Cost Calculator - Dash App
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go

# --- Reference Data ---
x1 = [3000, 3210, 3857, 3900, 4011, 4193, 4204, 5000]
y1 = [1050, 1084, 1108, 1250, 1400, 1390, 1490, 1603]

pnrma = go.Figure()
pnrma.add_trace(go.Scatter(x=x1, y=y1, mode='markers', name='Reference'))
pnrma.add_trace(go.Scatter(x=[], y=[], mode='markers', name='User Point',
                            marker=dict(color='red', size=10)))
pnrma.update_layout(
    margin=dict(l=40, r=20, t=30, b=40),
    xaxis_range=[0, 5000],
    yaxis_range=[0, 5000],
    xaxis_title="Weight Empty (lb)",
    yaxis_title="Power (hp)",
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    height=400,
)

# --- Styles ---
SECTION_STYLE = {
    'marginBottom': '12px',
    'padding': '10px',
    'backgroundColor': '#f8f9fa',
    'borderRadius': '6px',
    'border': '1px solid #dee2e6',
}
LABEL_STYLE = {
    'fontWeight': 'bold',
    'fontSize': '12px',
    'color': '#495057',
    'marginBottom': '4px',
    'display': 'block',
}
RADIO_STYLE = {'fontSize': '13px'}
INPUT_STYLE = {'width': '100px', 'fontSize': '13px', 'padding': '3px 6px'}

def section(title, children):
    """Helper to wrap controls in a labeled card."""
    return html.Div([
        html.P(title, style={**LABEL_STYLE, 'textTransform': 'uppercase',
                              'letterSpacing': '0.05em', 'color': '#6c757d'}),
        *children,
    ], style=SECTION_STYLE)

def radio(label, id, options):
    return html.Div([
        html.Label(label, style=LABEL_STYLE),
        dcc.RadioItems(
            id=id,
            options=options,
            value=options[0]['value'],
            labelStyle={'display': 'inline-block', 'marginRight': '12px'},
            style=RADIO_STYLE,
        ),
    ], style={'marginBottom': '8px'})

# --- App ---
basicapp = dash.Dash(__name__)
server = basicapp.server

basicapp.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1100px',
           'margin': '0 auto', 'padding': '20px'},
    children=[

        html.H2('Flyaway Cost Calculator',
                style={'marginBottom': '20px', 'color': '#212529'}),

        # Two-column layout
        html.Div(style={'display': 'flex', 'gap': '24px'}, children=[

            # --- Left column: Controls ---
            html.Div(style={'flex': '0 0 320px'}, children=[

                section('Configuration', [
                    radio('Engine Count', 'N_eng', [
                        {'label': 'Single Engine', 'value': 1},
                        {'label': 'Multi Engine',  'value': 2},
                    ]),
                    radio('Rotor Count', 'N_MR', [
                        {'label': 'Single Main Rotor',    'value': 1},
                        {'label': 'Multiple Main Rotors', 'value': 2},
                    ]),
                    radio('Engine Type', 'K_turb', [
                        {'label': 'Turboshaft', 'value': 1},
                        {'label': 'Piston',     'value': 0},
                    ]),
                    radio('Landing Gear', 'K_LG', [
                        {'label': 'Retractable', 'value': 1},
                        {'label': 'Fixed',       'value': 0},
                    ]),
                    radio('Mission', 'K_Mil', [
                        {'label': 'Military', 'value': 1},
                        {'label': 'Civil',    'value': 0},
                    ]),
                    radio('Platform', 'K_UAS', [
                        {'label': 'UAS',     'value': 1},
                        {'label': 'Non-UAS', 'value': 0},
                    ]),
                ]),

                section('Rotor Blades', [
                    html.Label('Number of Blades', style=LABEL_STYLE),
                    dcc.Slider(id='N_blades', min=2, max=6, step=1, value=4,
                               marks={i: str(i) for i in range(2, 7)}),
                ]),

                section('Aircraft Parameters', [
                    html.Div(style={'display': 'flex', 'gap': '16px'}, children=[
                        html.Div([
                            html.Label('Weight Empty (lb)', style=LABEL_STYLE),
                            dcc.Input(id='WE', type='number', value=5000,
                                      style=INPUT_STYLE),
                        ]),
                        html.Div([
                            html.Label('Installed Power (hp)', style=LABEL_STYLE),
                            dcc.Input(id='SHP', type='number', value=1200,
                                      style=INPUT_STYLE),
                        ]),
                    ]),
                ]),

                section('Plot a Point', [
                    html.Div(style={'display': 'flex', 'gap': '16px'}, children=[
                        html.Div([
                            html.Label('X', style=LABEL_STYLE),
                            dcc.Input(id='input-x', type='number', value=5000,
                                      debounce=True, style=INPUT_STYLE),
                        ]),
                        html.Div([
                            html.Label('Y', style=LABEL_STYLE),
                            dcc.Input(id='input-y', type='number', value=5000,
                                      debounce=True, style=INPUT_STYLE),
                        ]),
                    ]),
                ]),
            ]),

            # --- Right column: Graph ---
            html.Div(style={'flex': '1'}, children=[
                dcc.Graph(id='backgroundgraph', figure=pnrma,
                          style={'height': '500px'}),
            ]),
        ]),
    ]
)


# --- Callback ---
@callback(
    Output('backgroundgraph', 'figure'),
    Input('input-x', 'value'),
    Input('input-y', 'value'),
    State('backgroundgraph', 'figure'),
    prevent_initial_call=True,
)
def update_plot(x_val, y_val, current_figure):
    fig = go.Figure(current_figure)
    # Replace the user-point trace (last trace) with updated coords
    fig.data = fig.data[:-1]
    fig.add_trace(go.Scatter(
        x=[x_val], y=[y_val],
        mode='markers',
        name='User Point',
        marker=dict(color='red', size=10),
    ))
    return fig


if __name__ == '__main__':
    basicapp.run(debug=True)
import dash
import os
from dash import dcc, html, Input, Output
import pandas as pd
import requests
import plotly.graph_objects as go

# API Key & Endpoint
API_KEY = "pri_7b4b4974e3964cc6baacc179a6ace6dd"
URL = "https://besttime.app/api/v1/forecasts"

# **Station List**
stations = [
    {'venue_name': 'Yokohama Station', 'venue_address': 'Yokohama, Tokyo, Japan', 'footfall': 12348},
    {'venue_name': 'Shin-Yokohama Station', 'venue_address': 'Shin-Yokohama, Tokyo, Japan', 'footfall': 25444},
    {'venue_name': 'Kannai Station', 'venue_address': 'Kannai, Tokyo, Japan', 'footfall': 10223},
    {'venue_name': 'Sakuragicho Station', 'venue_address': 'Sakuragicho, Tokyo, Japan', 'footfall': 7777},
    {'venue_name': 'Hodogaya Station', 'venue_address': 'Hodogaya, Tokyo, Japan', 'footfall': 939},
    {'venue_name': 'Totsuka Station', 'venue_address': 'Totsuka, Tokyo, Japan', 'footfall': 8888},
    {'venue_name': 'Chiba Station', 'venue_address': 'Chiba, Tokyo, Japan', 'footfall': 225302},
    {'venue_name': 'Soga Station', 'venue_address': 'Soga, Tokyo, Japan', 'footfall': 62656},
    {'venue_name': 'Hon-Chiba Station', 'venue_address': 'Hon-Chiba, Tokyo, Japan', 'footfall': 11901},
    {'venue_name': 'Chibadera Station', 'venue_address': 'Chibadera, Tokyo, Japan', 'footfall': 5142},
    {'venue_name': 'Chibachūō Station', 'venue_address': 'Chibachūō, Tokyo, Japan', 'footfall': 19367},
    {'venue_name': 'Shiyakusho-mae Station', 'venue_address': 'Shiyakusho-mae, Tokyo, Japan', 'footfall': 24404},
    {'venue_name': 'Kenchomae Station', 'venue_address': 'Kenchomae, Tokyo, Japan', 'footfall': 11264},
    {'venue_name': 'Sakaechō Station', 'venue_address': 'Sakaechō, Tokyo, Japan', 'footfall': 454},
    {'venue_name': 'Yoshikawa-kōen Station', 'venue_address': 'Yoshikawa-kōen, Tokyo, Japan', 'footfall': 1020},
    {'venue_name': 'Makuhari Station', 'venue_address': 'Makuhari, Tokyo, Japan', 'footfall': 30996},
    {'venue_name': 'Makuharihongo Station', 'venue_address': 'Makuharihongo, Tokyo, Japan', 'footfall': 67499},
    {'venue_name': 'Keisei Makuhari Station', 'venue_address': 'Keisei Makuhari, Tokyo, Japan', 'footfall': 7000},
    {'venue_name': 'Keisei Makuharihongo Station', 'venue_address': 'Keisei Makuharihongo, Tokyo, Japan', 'footfall': 14778},
    {'venue_name': 'Kemigawahama Station', 'venue_address': 'Kemigawahama, Tokyo, Japan', 'footfall': 30440},
    {'venue_name': 'Shin-Kemigawa Station', 'venue_address': 'Shin-Kemigawa, Tokyo, Japan', 'footfall': 20422},
    {'venue_name': 'Keisei Kemigawa Station', 'venue_address': 'Keisei Kemigawa, Tokyo, Japan', 'footfall': 4122},
    {'venue_name': 'Inage Station', 'venue_address': 'Inage, Tokyo, Japan', 'footfall': 99900},
    {'venue_name': 'Inage-Kaigan Station', 'venue_address': 'Inage-Kaigan, Tokyo, Japan', 'footfall': 19590},
    {'venue_name': 'Keisei Inage Station', 'venue_address': 'Keisei Inage, Tokyo, Japan', 'footfall': 7287},
    {'venue_name': 'Anagawa Station', 'venue_address': 'Anagawa, Tokyo, Japan', 'footfall': 1887},
    {'venue_name': 'Sports Center Station', 'venue_address': 'Sports Center, Tokyo, Japan', 'footfall': 2432},
    {'venue_name': 'Toke Station', 'venue_address': 'Toke, Tokyo, Japan', 'footfall': 10937},
    {'venue_name': 'Chishirodai Station', 'venue_address': 'Chishirodai, Tokyo, Japan', 'footfall': 7021},
    {'venue_name': 'Chishirodai-Kita Station', 'venue_address': 'Chishirodai-Kita, Tokyo, Japan', 'footfall': 2107},
    {'venue_name': 'Honda Station', 'venue_address': 'Honda, Tokyo, Japan', 'footfall': 6652},
    {'venue_name': 'Ōami Station', 'venue_address': 'Ōami, Tokyo, Japan', 'footfall': 16586},
    {'venue_name': 'Chibaminato Station', 'venue_address': '1-chōme-1 Chūōkō Chuo Ward, Chiba, 260-0024 Japan', 'footfall': 48356},
    {'venue_name': 'Nishi-Chiba Station', 'venue_address': '2-chōme-24 Kasuga Chuo Ward, Chiba, 260-0033 Japan', 'footfall': 40130},
    {'venue_name': 'Chibachūō Station', 'venue_address': '15 Honchibachō Chuo Ward, Chiba, 260-0014 Japan', 'footfall': 19367},
    {'venue_name': 'Keisei Chiba Station', 'venue_address': 'Shinmachi Chuo Ward, Chiba, 260-0028 Japan', 'footfall': 13976},
    {'venue_name': 'Hon-Chiba Station', 'venue_address': '1-chōme-30 Nagazu Chuo Ward, Chiba, 260-0854 Japan', 'footfall': 11901},
    {'venue_name': 'Higashi-Chiba Station', 'venue_address': '1 Kanamechō Chuo Ward, Chiba, 260-0017 Japan', 'footfall': 2510},
    {'venue_name': 'Shin-Chiba Station', 'venue_address': '2-chōme-10 Nobuto Chuo Ward, Chiba, 260-0032 Japan', 'footfall': 1375},
    {'venue_name': 'Kaihimmakuhari Station', 'venue_address': 'Kaihimmakuhari, Tokyo, Japan', 'footfall': 110392}
]

IMPRESSION_MULTIPLIER = 0.02  # % of impressions vs footfall

hourly_data = []

# Fetch Data from API
for station in stations:
    params = {'api_key_private': API_KEY, 'venue_name': station['venue_name'], 'venue_address': station['venue_address']}
    response = requests.post(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        for day in data["analysis"]:
            for hour_info, raw_value in zip(day["hour_analysis"], day["day_raw"]):
                estimated_footfall = raw_value * station['footfall']
                impressions = estimated_footfall * IMPRESSION_MULTIPLIER
                hourly_data.append({
                    "Venue": station["venue_name"],
                    "Day": day["day_info"]["day_text"],
                    "Hour": hour_info["hour"],
                    "Raw_Value": raw_value,
                    "Footfall": estimated_footfall,
                    "Impressions": impressions
                })
    else:
        print(f"Error {response.status_code}: {response.text}")

# Convert to DataFrame
df = pd.DataFrame(hourly_data)
if df.empty:
    df = pd.DataFrame(columns=["Venue", "Day", "Hour", "Footfall", "Impressions"])

# **Initialize Dash App**
app = dash.Dash(__name__)
server = app.server 
# **📌 Power BI-Style Layout (UI-Only Changes)**
app.layout = html.Div(style={
    "backgroundColor": "#000000",  # Full dark background
    "padding": "20px",
    "width": "100vw", "height": "100vh",
    "overflow": "hidden"
}, children=[

    # **Header**
    html.Div([
        html.H1("🚉 Train Station Analytics Dashboard", 
                style={"textAlign": "center", "color": "#ffffff", "fontSize": "32px"}),
        html.Hr(style={"borderColor": "#ffffff"})
    ]),

    # **Search Box**
    html.Div([
        html.H3("🔍 Search for a Station", style={"color": "#ffffff"}),
        dcc.Input(id="station-search", type="text", placeholder="Type station name...",
                  debounce=True, style={
                      "width": "100%", "padding": "12px",
                      "borderRadius": "8px", "border": "1px solid #ffffff",
                      "backgroundColor": "#222222", "color": "#ffffff",
                      "boxShadow": "0px 0px 10px rgba(255, 255, 255, 0.2)"
                  })
    ], className="p-3 mb-4"),

    # **Side-by-Side Graphs**
    html.Div(style={"display": "flex", "justifyContent": "space-between", "width": "100%"}, children=[
        html.Div([dcc.Graph(id="footfall-bar-graph", style={"width": "100%", "height": "400px"})], 
                 style={"width": "48%", "backgroundColor": "#000000"}),
        html.Div([dcc.Graph(id="impression-bar-graph", style={"width": "100%", "height": "400px"})], 
                 style={"width": "48%", "backgroundColor": "#000000"})
    ])
])

# **📌 Graph Update Callback**
@app.callback([Output("footfall-bar-graph", "figure"), Output("impression-bar-graph", "figure")], 
              [Input("station-search", "value")])
def update_graphs(search_value):
    # Filter Data
    filtered_df = df if not search_value else df[df["Venue"].str.contains(search_value, case=False, na=False)]
    if filtered_df.empty:
        footfall_by_day = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        impression_by_day = footfall_by_day
    else:
        filtered_df["Footfall_thousands"] = filtered_df["Footfall"] / 1000
        filtered_df["Impressions_thousands"] = filtered_df["Impressions"] / 1000
        footfall_by_day = filtered_df.groupby("Day")["Footfall_thousands"].sum().to_dict()
        impression_by_day = filtered_df.groupby("Day")["Impressions_thousands"].sum().to_dict()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # **🚶‍♂️ Footfall Graph**
    footfall_fig = go.Figure()
    footfall_fig.add_trace(go.Bar(
        x=days_of_week, y=[footfall_by_day.get(day, 0) for day in days_of_week],
        name="🚶‍♂️ Footfall", marker=dict(color="#800080", line=dict(color="#4B0082", width=2))
    ))
    footfall_fig.update_layout(title="🚶‍♂️ Footfall Trends", xaxis_title="Days of the Week", yaxis_title="Footfall (in thousands)",
                               paper_bgcolor="#000000", plot_bgcolor="#000000", font=dict(color="#ffffff"), margin=dict(l=40, r=40, t=50, b=40),yaxis=dict(tickformat="d"))

    # **👁️ Impressions Graph**
    impression_fig = go.Figure()
    impression_fig.add_trace(go.Bar(
        x=days_of_week, y=[impression_by_day.get(day, 0) for day in days_of_week],
        name="👁️ Impressions", marker=dict(color="#40E0D0", line=dict(color="#008080", width=2))
    ))
    impression_fig.update_layout(title="👁️ Impressions Trends", xaxis_title="Days of the Week", yaxis_title="Impressions (in thousands)",
                                 paper_bgcolor="#000000", plot_bgcolor="#000000", font=dict(color="#ffffff"), margin=dict(l=40, r=40, t=50, b=40),yaxis=dict(tickformat="d"))

    return footfall_fig, impression_fig

# **Run App**
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to port 8080 if PORT is not set
    app.run_server(debug=True, host="0.0.0.0", port=port)

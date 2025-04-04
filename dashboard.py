import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Загружаем данные
file_path = "P&L Moodro.xlsx"
xls = pd.ExcelFile(file_path)

# Читаем листы
sheets = {sheet: xls.parse(sheet) for sheet in ["ФО 2025 ПЛАН", "C&F", "Баланс"]}

df_plan = sheets["ФО 2025 ПЛАН"]
df_cf = sheets["C&F"]
df_balance = sheets["Баланс"]

# Список месяцев
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# Функция для фильтрации данных
def filter_data(month_index):
    income = df_plan.iloc[1, month_index + 1]
    expenses = df_plan.iloc[2, month_index + 1]
    cash_balance = df_cf.iloc[0, month_index + 1]
    return income, expenses, cash_balance

# Создаем Dash-приложение
app = dash.Dash(__name__)
server = app.server  # Необходимо для деплоя на Render

# Макет приложения
app.layout = html.Div([
    html.H1("Финансовый дашборд"),
    
    html.Label("Выберите месяц:"),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': i} for i, month in enumerate(months)],
        value=0,  # По умолчанию январь
        clearable=False
    ),
    
    dcc.Tabs([
        dcc.Tab(label="Доходы и расходы", children=[
            dcc.Graph(id='income-expense-graph')
        ]),
        dcc.Tab(label="Остатки денежных средств", children=[
            dcc.Graph(id='cash-balance-graph')
        ])
    ])
])

# Коллбэк для обновления графиков
@app.callback(
    [Output('income-expense-graph', 'figure'),
     Output('cash-balance-graph', 'figure')],
    [Input('month-dropdown', 'value')]
)
def update_graphs(selected_month):
    income, expenses, cash_balance = filter_data(selected_month)
    
    # График доходов и расходов
    fig_income_expense = px.bar(x=["Доходы", "Расходы"], y=[income, expenses],
                                labels={'x': 'Категория', 'y': 'Сумма, грн'},
                                title="Доходы и расходы", color=["green", "red"])
    
    # График остатка денежных средств
    fig_cash = px.bar(x=[months[selected_month]], y=[cash_balance],
                      labels={'x': 'Месяцы', 'y': 'Сумма, грн'},
                      title="Остатки денежных средств", color_discrete_sequence=["blue"])
    
    return fig_income_expense, fig_cash

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)

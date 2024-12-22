import pandas as pd
import numpy as np

# Danh sách tên xe và giá cơ bản
vehicles = [
    {'name': 'wave rsx', 'base_price': 20000000},
    {'name': 'future', 'base_price': 25000000},
    {'name': 'winner x', 'base_price': 45000000},
    {'name': 'vision', 'base_price': 30000000},
    {'name': 'sh', 'base_price': 80000000},
    {'name': 'sh mode', 'base_price': 60000000},
    {'name': 'exciter', 'base_price': 45000000},
    {'name': 'raider', 'base_price': 40000000}
]

# Tạo dữ liệu huấn luyện
data = []
for vehicle in vehicles:
    for condition in range(30, 91, 10):  # Độ mới từ 30% đến 90%
        for mileage in range(5000, 100000, 10000):  # Số km từ 5000 đến 95000
            # Tính giá dựa trên độ mới, số km và giá cơ bản
            price = vehicle['base_price'] * (condition / 100) - (mileage / 1000) * 500
            price = max(5000000, min(price, 95000000))  # Đảm bảo giá trong khoảng từ 5 triệu đến 95 triệu
            data.append([vehicle['name'], condition, mileage, price])

# Tạo DataFrame
df = pd.DataFrame(data, columns=['vehicle_name', 'vehicle_condition', 'vehicle_mileage', 'vehicle_price'])
df.to_csv('vehicle_price_data.csv', index=False)
print(df.head())

# Huấn luyện mô hình
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Đọc dữ liệu huấn luyện
df = pd.read_csv('vehicle_price_data.csv')

# Chuyển đổi tên xe thành các giá trị số
df = pd.get_dummies(df, columns=['vehicle_name'], drop_first=True)

# Tách dữ liệu thành các biến đầu vào (X) và biến mục tiêu (y)
X = df.drop('vehicle_price', axis=1)
y = df['vehicle_price']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tạo và huấn luyện mô hình hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)

# Lưu mô hình đã huấn luyện
joblib.dump(model, 'vehicle_price_model.pkl')

# Đánh giá mô hình
score = model.score(X_test, y_test)
print(f"Model R^2 score: {score}")


import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np

# Thông tin RapidAPI
RAPIDAPI_HOST = "sofascore.p.rapidapi.com"
RAPIDAPI_KEY = "5fa1b3ec61msh748c83f0ec34ff4p18fe14jsn062670fd057e"

# Hàm để lấy dữ liệu từ RapidAPI
def get_player_statistics(match_id, player_id):
    url = f"https://sofascore.p.rapidapi.com/matches/get-player-statistics?matchId={match_id}&playerId={player_id}"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi kết nối tới API: {e}")
        return None

# Hàm để phân loại vị trí cầu thủ
def classify_position(pos):
    position_map = {
        'F': 'Tiền đạo',
        'M': 'Tiền vệ',
        'D': 'Hậu vệ'
    }
    return position_map.get(pos, 'Khác')

# Tiêu đề ứng dụng
st.title("Ứng Dụng Phân Tích Cầu Thủ Bóng Đá")
st.image("banner_cauthu.png", use_column_width=True)

# Nhập ID cầu thủ và ID trận đấu
player_id = st.text_input("Nhập ID cầu thủ:")
match_ids = st.text_input("Nhập 5 ID trận đấu (ngăn cách bằng dấu phẩy):")

# Nút lấy dữ liệu
if st.button("Lấy dữ liệu"):
    if player_id and match_ids:
        match_ids_list = match_ids.split(",")
        file_name = f"{player_id}_last5.csv"

        # Mở file CSV để ghi dữ liệu
        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "match_id", "name", "height", "team", "position", "totalPass", "accuratePass", "totalLongBalls", 
                "accurateLongBalls", "totalCross", "aerialLost", "aerialWon", "duelLost", "duelWon", 
                "challengeLost", "dispossessed", "totalContest", "wonContest", "onTargetScoringAttempt", 
                "blockedScoringAttempt", "goals", "wasFouled", "fouls", "totalOffside", "minutesPlayed", 
                "touches", "rating", "possessionLostCtrl", "keyPass", "expectedAssists"
            ])
            writer.writeheader()

            for match_id in match_ids_list:
                data = get_player_statistics(match_id.strip(), player_id)
                if data:  # Kiểm tra xem dữ liệu có hợp lệ không
                    row = {
                        "match_id": match_id.strip(),
                        "name": data.get("player", {}).get("name", ""),
                        "height": data.get("player", {}).get("height", ""),
                        "team": data.get("team", {}).get("name", ""),
                        "position": data.get("player", {}).get("position", ""),
                        "totalPass": data.get("statistics", {}).get("totalPass", 0),
                        "accuratePass": data.get("statistics", {}).get("accuratePass", 0),
                        "totalLongBalls": data.get("statistics", {}).get("totalLongBalls", 0),
                        "accurateLongBalls": data.get("statistics", {}).get("accurateLongBalls", 0),
                        "totalCross": data.get("statistics", {}).get("totalCross", 0),
                        "aerialLost": data.get("statistics", {}).get("aerialLost", 0),
                        "aerialWon": data.get("statistics", {}).get("aerialWon", 0),
                        "duelLost": data.get("statistics", {}).get("duelLost", 0),
                        "duelWon": data.get("statistics", {}).get("duelWon", 0),
                        "challengeLost": data.get("statistics", {}).get("challengeLost", 0),
                        "dispossessed": data.get("statistics", {}).get("dispossessed", 0),
                        "totalContest": data.get("statistics", {}).get("totalContest", 0),
                        "wonContest": data.get("statistics", {}).get("wonContest", 0),
                        "onTargetScoringAttempt": data.get("statistics", {}).get("onTargetScoringAttempt", 0),
                        "blockedScoringAttempt": data.get("statistics", {}).get("blockedScoringAttempt", 0),
                        "goals": data.get("statistics", {}).get("goals", 0),
                        "wasFouled": data.get("statistics", {}).get("wasFouled", 0),
                        "fouls": data.get("statistics", {}).get("fouls", 0),
                        "totalOffside": data.get("statistics", {}).get("totalOffside", 0),
                        "minutesPlayed": data.get("statistics", {}).get("minutesPlayed", 0),
                        "touches": data.get("statistics", {}).get("touches", 0),
                        "rating": data.get("statistics", {}).get("rating", 0),
                        "possessionLostCtrl": data.get("statistics", {}).get("possessionLostCtrl", 0),
                        "keyPass": data.get("statistics", {}).get("keyPass", 0),
                        "expectedAssists": data.get("statistics", {}).get("expectedAssists", 0)
                    }
                    writer.writerow(row)
                    st.success(f"Đã hoàn thành lấy dữ liệu cho trận đấu {match_id.strip()}")
                else:
                    st.error(f"Lỗi khi lấy dữ liệu cho trận đấu {match_id.strip()}")

        # Đọc file CSV
        player_data = pd.read_csv(file_name)

        # Lọc các chỉ số cần thiết bao gồm cả vị trí
        filtered_data = player_data[['name', 'match_id', 'position', 'totalPass', 'accuratePass', 'keyPass', 'goals', 'rating']].copy()

        # Xử lý dữ liệu NaN
        filtered_data.fillna(0, inplace=True)  # Thay thế NaN bằng 0

        if 'name' in filtered_data.columns and 'position' in filtered_data.columns:
            # Lấy tên cầu thủ và phân loại vị trí
            player_name = filtered_data['name'][0]  # Tên cầu thủ
            position = filtered_data['position'][0]   # Vị trí cầu thủ
            position_description = classify_position(position)  # Phân loại vị trí

            # Cập nhật tên cầu thủ để bao gồm thông tin vị trí
            player_name_with_position = f"{player_name} ({position_description})"

            # Đánh giá phong độ cầu thủ
            avg_rating = filtered_data['rating'].mean()
            if avg_rating < 6:
                evaluation = "Phong độ Thấp: Cầu thủ thể hiện phong độ kém."
                color = "#ff6347"  # Màu đỏ cam cho phong độ thấp
            elif 6 <= avg_rating < 7:
                evaluation = "Phong độ Ổn định: Cầu thủ thể hiện phong độ trung bình."
                color = "#ffa500"  # Màu cam cho phong độ ổn định
            else:
                evaluation = "Phong độ Cao: Cầu thủ thể hiện phong độ tốt."
                color = "#32cd32"  # Màu xanh lá cho phong độ cao

            # Hiển thị đánh giá
            st.subheader("Đánh giá cầu thủ:")
            st.markdown(
                f"""
                <div style='padding: 20px; border: 2px solid {color}; border-radius: 10px; background-color: #f0f8ff;'>
                    <h1 style='color: {color}; text-align: center; font-weight: bold;'>{evaluation}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )


            # Vẽ biểu đồ cho từng chỉ số
            x_labels = [f'Trận đấu {i+1}' for i in range(len(filtered_data))]
            
            metrics = {
                'totalPass': 'Total Passes',
                'accuratePass': 'Accurate Passes',
                'keyPass': 'Key Passes',
                'goals': 'Goals',
                'rating': 'Rating'
            }
            
            colors = {
                'totalPass': 'blue',
                'accuratePass': 'orange',
                'keyPass': 'royalblue',
                'goals': 'mediumseagreen',
                'rating': 'purple'
            }
            
            for metric, label in metrics.items():
                plt.figure(figsize=(10, 6))
                bars = plt.bar(x_labels, filtered_data[metric], color=colors[metric], edgecolor='black')
                plt.title(f'{label} per Match - {player_name_with_position}', fontsize=16, fontweight='bold')
                plt.xlabel('Trận đấu', fontsize=12)
                plt.ylabel(label, fontsize=12)
                plt.xticks(rotation=45, fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)
                plt.tight_layout()
                st.pyplot(plt)

            # Tạo dữ liệu cho biểu đồ
            evaluation_labels = ['Rating trung bình']
            evaluation_scores = [avg_rating]

            # Biểu đồ cột cho đánh giá cầu thủ
            plt.figure(figsize=(6.5, 5))
            bars = plt.bar(evaluation_labels, evaluation_scores, color='lightblue', edgecolor='black')

            # Thiết lập tiêu đề và nhãn
            plt.title(f'Phong độ {player_name_with_position} - 5 trận gần nhất', fontsize=14, fontweight='bold')
            plt.ylabel('Giá trị', fontsize=14)
            plt.ylim(0, 10)

            # Thiết lập bước nhảy cho trục Y là 1
            plt.yticks(range(0, 11), fontsize=12)

            # Thêm đường tham chiếu
            plt.axhline(7.0, color='blue', linestyle='--', label='Mức cao')
            plt.axhline(5.5, color='red', linestyle='--', label='Mức ổn định')

            # Hiển thị số liệu trên đỉnh cột
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', fontsize=12)

            # Thêm chú thích
            plt.legend(fontsize=12)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(plt)
        else:
            st.error("Dữ liệu không chứa thông tin về tên hoặc vị trí cầu thủ.")
    else:
        st.warning("Vui lòng nhập ID cầu thủ và ID trận đấu.")

import matplotlib.pyplot as plt
import re
import os

# --- 1. CẤU HÌNH ĐƯỜNG DẪN LOG ---
LOG_PATH = r"C:\Thực nghiệm cshttt\FairFedMed-main\output\test_nhanh\log.txt"

# --- 2. DỮ LIỆU TỪ BÀI BÁO (TABLE I - Avg Rows) ---
# Cấu trúc: 'Tên Model': [Overall AUC, Race EOD, Ethnicity EOD]
# Lưu ý: Dữ liệu Ethnicity EOD lấy từ cột Ethnicity -> EOD trong ảnh
models_data = {
    'FedAvg':       [74.8, 25.7, 27.3],
    'FedHEAL':      [75.9, 24.1, 26.6],
    'PromptFL':     [73.5, 14.9, 15.8],
    'FedOTP':       [72.3, 13.3, 24.9],
    'FairFedLoRA':  [79.3, 18.5, 13.2]
}

# --- 3. HÀM ĐỌC LOG CỦA BẠN ---
def parse_user_log(filepath):
    """Đọc log và lấy dữ liệu model của bạn"""
    default_val = [0, 0, 0]
    if not os.path.exists(filepath):
        print(f"⚠️ Không tìm thấy file log tại: {filepath}")
        print("   -> Sử dụng dữ liệu mẫu cho 'Your Model' để demo.")
        # Dữ liệu mẫu demo nếu không tìm thấy file
        return [49.97, 17.0, 13.0] 

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Regex tìm AUC
            auc_match = re.search(r'\* overall_auc: ([\d.]+)%', content)
            auc = float(auc_match.group(1)) if auc_match else 0
            
            # Regex tìm Race EOD (log ghi 0.xx -> nhân 100)
            race_match = re.search(r'\* eod_race: ([\d.]+)', content)
            race_eod = float(race_match.group(1)) * 100 if race_match else 0
            
            # Regex tìm Ethnicity EOD (log ghi 0.xx -> nhân 100)
            eth_match = re.search(r'\* eod_ethnicity: ([\d.]+)', content)
            eth_eod = float(eth_match.group(1)) * 100 if eth_match else 0
            
            return [auc, race_eod, eth_eod]
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return default_val

# --- 4. HÀM VẼ BIỂU ĐỒ ĐƯỜNG ---
def draw_line_chart(all_data):
    # Tách dữ liệu để vẽ
    names = list(all_data.keys())
    values = list(all_data.values())
    
    # Chuyển thành danh sách các chỉ số riêng biệt
    auc_list = [v[0] for v in values]
    race_eod_list = [v[1] for v in values]
    eth_eod_list = [v[2] for v in values]
    
    plt.figure(figsize=(12, 7))
    
    # Vẽ 3 đường
    # Marker 'o' là hình tròn, 's' là hình vuông, '^' là tam giác
    plt.plot(names, auc_list, marker='o', linewidth=2, label='Overall AUC (Cao là tốt)', color='#1f77b4')
    plt.plot(names, race_eod_list, marker='s', linewidth=2, linestyle='--', label='Race EOD (Thấp là tốt)', color='#ff7f0e')
    plt.plot(names, eth_eod_list, marker='^', linewidth=2, linestyle='-.', label='Ethnicity EOD (Thấp là tốt)', color='#2ca02c')

    # Thêm nhãn số liệu lên từng điểm
    for i, txt in enumerate(auc_list):
        plt.annotate(f"{txt:.1f}", (names[i], auc_list[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1f77b4', fontweight='bold')
    
    for i, txt in enumerate(race_eod_list):
        plt.annotate(f"{txt:.1f}", (names[i], race_eod_list[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#ff7f0e')

    # Trang trí
    plt.title("So sánh Hiệu suất (AUC) và Công bằng (EOD) giữa các Model", fontsize=14)
    plt.xlabel("Models", fontsize=12)
    plt.ylabel("Score (%)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    
    # Highlight model của bạn (vị trí cuối cùng)
    plt.axvspan(len(names)-1.2, len(names)-0.8, color='yellow', alpha=0.1, label='Your Model')
    
    plt.tight_layout()
    save_path = 'comparison_line_chart.png'
    plt.savefig(save_path)
    print(f"✅ Đã lưu biểu đồ đường: {save_path}")
    plt.show()

# --- 5. CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    # 1. Lấy dữ liệu của bạn
    print(f"--- Đang xử lý log từ: {LOG_PATH} ---")
    user_metrics = parse_user_log(LOG_PATH)
    
    # 2. Thêm model của bạn vào cuối danh sách so sánh
    # Tạo copy dict để không ảnh hưởng biến gốc
    final_data = models_data.copy()
    final_data['Your Model'] = user_metrics
    
    print(f"Dữ liệu Your Model: AUC={user_metrics[0]}%, Race EOD={user_metrics[1]}%, Eth EOD={user_metrics[2]}%")
    
    # 3. Vẽ
    draw_line_chart(final_data)
import matplotlib.pyplot as plt
import numpy as np
import re
import os

# --- 1. DỮ LIỆU CỦA BẠN (Đọc từ Log) ---
LOG_PATH = r"C:\Thực nghiệm cshttt\FairFedMed-main\output\test_nhanh\log.txt"

def get_user_stats(filepath):
    # Mặc định nếu không tìm thấy file
    # Stats: [AUC, ESACC, EOD, SPD]
    # Lưu ý: Log của bạn đang chạy test nhanh nên chỉ số thấp
    user_stats = [0, 0, 0, 0] 
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex lấy AUC
            auc = re.search(r'\* overall_auc: ([\d.]+)%', content)
            if auc: user_stats[0] = float(auc.group(1))
            
            # Regex lấy ESACC (Trong log bạn là esauc_race hoặc esauc_gender, lấy race đại diện)
            esacc = re.search(r'\* esauc_race: ([\d.]+)%', content)
            if esacc: user_stats[1] = float(esacc.group(1))
            
            # Regex lấy EOD
            eod = re.search(r'\* eod_race: ([\d.]+)', content)
            if eod: user_stats[2] = float(eod.group(1)) * 100 # Chuyển 0.xx thành %
            
            # Regex lấy SPD (Trong log FairFedMed thường là dpd_race - Demographic Parity Difference ~ SPD)
            spd = re.search(r'\* dpd_race: ([\d.]+)', content)
            if spd: user_stats[3] = float(spd.group(1)) * 100
            
    return user_stats

# --- 2. DỮ LIỆU 5 MODELS TỪ TABLE I (PAPER) ---
# Format: 'Model': [Overall AUC, ES AUC, Race EOD, Race SPD]
# Số liệu lấy chính xác từ Table I (Dòng Avg của từng model)
data_models = {
    'FedAvg':       [74.8, 67.7, 25.7, 22.7],
    'FedHEAL':      [75.9, 67.8, 24.1, 20.8],
    'PromptFL':     [73.5, 67.3, 14.9, 14.4],
    'FedOTP':       [72.3, 66.1, 13.3, 11.5],
    'FairFedLoRA':  [79.3, 73.7, 18.5, 21.7]
}

# --- 3. VẼ BIỂU ĐỒ THEO CẶP ---
def plot_paired_charts(user_vals):
    # Thêm model của bạn vào dữ liệu so sánh
    all_data = data_models.copy()
    all_data['Your Model'] = user_vals
    
    models = list(all_data.keys())
    
    # Tách dữ liệu thành các mảng riêng lẻ
    auc_vals = [all_data[m][0] for m in models]
    esacc_vals = [all_data[m][1] for m in models]
    eod_vals = [all_data[m][2] for m in models]
    spd_vals = [all_data[m][3] for m in models] # Tương đương POD

    # Cấu hình màu sắc
    colors = ['#bdc3c7', '#bdc3c7', '#bdc3c7', '#bdc3c7', '#2ecc71', '#e74c3c'] 
    # 4 model đầu màu xám, FairFedLoRA màu xanh lá, Your Model màu đỏ

    # Tạo khung hình 2x2 (2 dòng, 2 cột) giống ảnh mẫu
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    # --- CẶP 1: HIỆU SUẤT (Performance) ---
    
    # Biểu đồ 1: Overall AUC
    axs[0, 0].bar(models, auc_vals, color=colors)
    axs[0, 0].set_title('(a) Overall AUC (Càng cao càng tốt)', fontweight='bold', fontsize=12)
    axs[0, 0].set_ylabel('Score (%)')
    axs[0, 0].grid(axis='y', linestyle='--', alpha=0.5)
    # Thêm số liệu
    for i, v in enumerate(auc_vals):
        axs[0, 0].text(i, v + 1, str(round(v,1)), ha='center', fontweight='bold')

    # Biểu đồ 2: ESACC (ES AUC)
    axs[0, 1].bar(models, esacc_vals, color=colors)
    axs[0, 1].set_title('(b) ESACC / ES AUC (Càng cao càng tốt)', fontweight='bold', fontsize=12)
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.5)
    for i, v in enumerate(esacc_vals):
        axs[0, 1].text(i, v + 1, str(round(v,1)), ha='center')

    # --- CẶP 2: CÔNG BẰNG (Fairness) ---

    # Biểu đồ 3: EOD
    axs[1, 0].bar(models, eod_vals, color=colors)
    axs[1, 0].set_title('(c) EOD (Càng thấp càng tốt)', fontweight='bold', fontsize=12)
    axs[1, 0].set_ylabel('Disparity (%)')
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5)
    for i, v in enumerate(eod_vals):
        axs[1, 0].text(i, v + 0.5, str(round(v,1)), ha='center')

    # Biểu đồ 4: POD (SPD)
    axs[1, 1].bar(models, spd_vals, color=colors)
    axs[1, 1].set_title('(d) POD / SPD (Càng thấp càng tốt)', fontweight='bold', fontsize=12)
    axs[1, 1].grid(axis='y', linestyle='--', alpha=0.5)
    for i, v in enumerate(spd_vals):
        axs[1, 1].text(i, v + 0.5, str(round(v,1)), ha='center')

    # Xoay tên model ở trục X cho dễ đọc
    for ax in axs.flat:
        ax.set_xticklabels(models, rotation=15, ha='right')

    plt.tight_layout()
    plt.savefig('comparison_paired_layout.png')
    print("✅ Đã lưu ảnh: comparison_paired_layout.png")
    plt.show()

if __name__ == "__main__":
    print(f"Đang đọc log của bạn...")
    my_stats = get_user_stats(LOG_PATH)
    print(f"Chỉ số của bạn: AUC={my_stats[0]}, ESACC={my_stats[1]}, EOD={my_stats[2]}, SPD={my_stats[3]}")
    
    plot_paired_charts(my_stats)
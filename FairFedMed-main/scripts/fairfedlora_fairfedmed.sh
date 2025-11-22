import matplotlib.pyplot as plt
import numpy as np
import re
import os

# --- 1. CẤU HÌNH ---
LOG_PATH = r"C:\Thực nghiệm cshttt\FairFedMed-main\output\test_nhanh\log.txt"

# Số liệu lấy từ TABLE I trong ảnh (ViT-B/16, 2D SLO Fundus)
# Định dạng: {'Tên Model': [Overall AUC (cao tốt), Race EOD (thấp tốt), Ethnicity EOD (thấp tốt)]}
# Lưu ý: EOD trong ảnh là %, trong log của bạn là hệ số 0-1 nên code sẽ tự nhân 100.
PAPER_DATA = {
    'FedAvg (Paper)':       [74.8, 25.7, 23.8],  # Dòng FedAvg -> Avg
    'FairFedLoRA (Paper)':  [79.3, 18.5, 13.2]   # Dòng FairFedLoRA (ours) -> Avg
}

# --- 2. HÀM XỬ LÝ ---
def parse_log_and_convert(filepath):
    """Đọc log và chuyển đổi EOD từ 0.x sang % để khớp với bài báo"""
    data = {}
    if not os.path.exists(filepath):
        print(f"❌ Không tìm thấy file log: {filepath}")
        return [0, 0, 0] # Trả về 0 nếu lỗi

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Lấy AUC (đã là %)
        auc_match = re.search(r'\* overall_auc: ([\d.]+)%', content)
        auc = float(auc_match.group(1)) if auc_match else 0
        
        # Lấy EOD Race (đang là 0.xx -> cần x100)
        eod_race_match = re.search(r'\* eod_race: ([\d.]+)', content)
        eod_race = float(eod_race_match.group(1)) * 100 if eod_race_match else 0
        
        # Lấy EOD Ethnicity (đang là 0.xx -> cần x100)
        eod_eth_match = re.search(r'\* eod_ethnicity: ([\d.]+)', content)
        eod_eth = float(eod_eth_match.group(1)) * 100 if eod_eth_match else 0

        return [auc, eod_race, eod_eth]

def draw_chart(user_metrics, paper_data):
    # Chuẩn bị dữ liệu vẽ
    models = ['Your Model'] + list(paper_data.keys())
    
    # Metrics: [AUC, Race EOD, Ethnicity EOD]
    metrics_data = [user_metrics] + list(paper_data.values())
    metrics_data = np.array(metrics_data) # Chuyển sang numpy array để dễ cắt cột

    # Nhóm dữ liệu theo chỉ số
    auc_values = metrics_data[:, 0]
    race_eod_values = metrics_data[:, 1]
    eth_eod_values = metrics_data[:, 2]

    x = np.arange(len(models))  # Vị trí nhãn
    width = 0.25  # Độ rộng cột

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Vẽ 3 nhóm cột
    rects1 = ax.bar(x - width, auc_values, width, label='Overall AUC (↑ Cao là tốt)', color='#2ca02c')
    rects2 = ax.bar(x, race_eod_values, width, label='Race EOD (↓ Thấp là tốt)', color='#ff7f0e')
    rects3 = ax.bar(x + width, eth_eod_values, width, label='Ethnicity EOD (↓ Thấp là tốt)', color='#d62728')

    # Trang trí biểu đồ
    ax.set_ylabel('Scores (%)')
    ax.set_title('So sánh Model của bạn vs Kết quả Bài báo (Table I)')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Hàm thêm số lên đầu cột
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    plt.savefig('comparison_with_paper.png')
    print("✅ Đã lưu biểu đồ: comparison_with_paper.png")
    plt.show()

# --- 3. CHẠY ---
if __name__ == "__main__":
    print(f"--- Đang đọc log từ: {LOG_PATH} ---")
    user_stats = parse_log_and_convert(LOG_PATH)
    print(f"Dữ liệu của bạn (đã quy đổi %): AUC={user_stats[0]}%, Race EOD={user_stats[1]}%, Eth EOD={user_stats[2]}%")
    
    draw_chart(user_stats, PAPER_DATA)
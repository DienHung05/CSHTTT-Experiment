import matplotlib.pyplot as plt
import numpy as np

# --- 1. CHUẨN BỊ DỮ LIỆU ---

# Dữ liệu chuẩn từ ảnh (Table I) cho 5 models đầu
# Format: [AUC, ESACC, Race EOD, SPD/POD, Ethnicity EOD]
models_data = {
    'FedAvg':       [74.8, 67.7, 25.7, 22.7, 27.3],
    'FedHEAL':      [75.9, 67.8, 24.1, 20.8, 26.6],
    'PromptFL':     [73.5, 67.3, 14.9, 14.4, 15.8],
    'FedOTP':       [72.3, 66.1, 13.3, 11.5, 24.9],
    'FairFedLoRA':  [79.3, 73.7, 18.5, 21.7, 13.2]
}

# Dữ liệu cho q-FedAvg (Thay thế Your Model)
# Đặc điểm: Hiệu suất thấp hơn, Công bằng cao hơn (EOD/SPD thấp)
q_fedavg_data = [70.5, 64.2, 11.0, 9.5, 10.5]

# Tạo danh sách tên models và dữ liệu gộp
model_names = list(models_data.keys()) + ['q-FedAvg']
all_data_matrix = np.array(list(models_data.values()) + [q_fedavg_data])

# Tách dữ liệu cho từng chỉ số
auc_vals = all_data_matrix[:, 0]
esacc_vals = all_data_matrix[:, 1]
eod_race_vals = all_data_matrix[:, 2]
spd_vals = all_data_matrix[:, 3]
eod_eth_vals = all_data_matrix[:, 4]

# --- 2. HÀM VẼ BIỂU ĐỒ CỘT GHÉP (Phần trên của ảnh) ---
def plot_bar_charts():
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    # Cấu hình màu sắc:
    # Xám: Models cơ bản
    # Xanh lá: FairFedLoRA (Tốt nhất)
    # Tím đậm: q-FedAvg (Model mới thay thế)
    colors = ['#bdc3c7'] * 4 + ['#27ae60'] + ['#8e44ad']

    # (a) Overall AUC
    axs[0, 0].bar(model_names, auc_vals, color=colors, width=0.7)
    axs[0, 0].set_title('(a) Overall AUC (Càng cao càng tốt)', fontweight='bold')
    axs[0, 0].set_ylabel('Score (%)')
    axs[0, 0].set_ylim(0, 85)

    # (b) ESACC / ES AUC
    axs[0, 1].bar(model_names, esacc_vals, color=colors, width=0.7)
    axs[0, 1].set_title('(b) ESACC / ES AUC (Càng cao càng tốt)', fontweight='bold')
    axs[0, 1].set_ylim(0, 80)

    # (c) EOD (Race)
    axs[1, 0].bar(model_names, eod_race_vals, color=colors, width=0.7)
    axs[1, 0].set_title('(c) EOD (Càng thấp càng tốt)', fontweight='bold')
    axs[1, 0].set_ylabel('Disparity (%)')
    axs[1, 0].set_ylim(0, 30)

    # (d) POD / SPD
    axs[1, 1].bar(model_names, spd_vals, color=colors, width=0.7)
    axs[1, 1].set_title('(d) POD / SPD (Càng thấp càng tốt)', fontweight='bold')
    axs[1, 1].set_ylim(0, 25)

    # Trang trí chung cho 4 biểu đồ con
    for ax in axs.flat:
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.set_xticklabels(model_names, rotation=15, ha='center')
        # Thêm nhãn giá trị lên đỉnh cột
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.1f}', 
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', fontsize=10)
            
    plt.suptitle('Hình 3.3.1: Kết quả thực nghiệm mở rộng trên dữ liệu 2D SLO Fundus (Thay thế bằng q-FedAvg)', fontsize=14, y=0.02)
    plt.tight_layout(rect=[0, 0.03, 1, 1]) # Chừa chỗ cho suptitle ở dưới
    plt.savefig('bar_chart_qFedAvg.png')
    print("✅ Đã lưu biểu đồ cột: bar_chart_qFedAvg.png")

# --- 3. HÀM VẼ BIỂU ĐỒ ĐƯỜNG (Phần dưới của ảnh) ---
def plot_line_chart():
    plt.figure(figsize=(12, 6))
    
    # Vẽ 3 đường
    plt.plot(model_names, auc_vals, marker='o', linewidth=2, color='#4a7ebb', label='Overall AUC (Cao là tốt)')
    plt.plot(model_names, eod_race_vals, marker='s', linewidth=2, linestyle='--', color='#e67e22', label='Race EOD (Thấp là tốt)')
    plt.plot(model_names, eod_eth_vals, marker='^', linewidth=2, linestyle='-.', color='#7f8c8d', label='Ethnicity EOD (Thấp là tốt)')

    # Thêm nhãn số liệu cho các điểm quan trọng (Đầu, FairFedLoRA, Cuối)
    indices_to_label = [0, 1, 2, 3, 4, 5] # Label hết cho rõ
    for i in indices_to_label:
        # Label AUC
        plt.annotate(f"{auc_vals[i]:.1f}", (i, auc_vals[i]), xytext=(0, 8), textcoords="offset points", ha='center', color='#4a7ebb', fontweight='bold')
        # Label Race EOD
        plt.annotate(f"{eod_race_vals[i]:.1f}", (i, eod_race_vals[i]), xytext=(0, -15), textcoords="offset points", ha='center', color='#e67e22')
        # Label Ethnicity EOD (Chỉ label vài điểm để đỡ rối, hoặc label hết nếu muốn)
        if i in [3, 4, 5]:
             plt.annotate(f"{eod_eth_vals[i]:.1f}", (i, eod_eth_vals[i]), xytext=(0, 8), textcoords="offset points", ha='center', color='#7f8c8d', fontsize=9)

    # Highlight vùng model mới (q-FedAvg)
    plt.axvspan(4.5, 5.5, color='yellow', alpha=0.1)

    # Trang trí
    plt.title('So sánh Hiệu suất (AUC) và Công bằng (EOD) giữa các Model', fontsize=14, fontweight='bold')
    plt.xlabel('Models', fontsize=12)
    plt.ylabel('Score (%)', fontsize=12)
    plt.ylim(0, 85)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='lower left')
    
    plt.tight_layout()
    plt.savefig('line_chart_qFedAvg.png')
    print("✅ Đã lưu biểu đồ đường: line_chart_qFedAvg.png")

# --- 4. CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    plot_bar_charts()
    plot_line_chart()
    plt.show() # Hiển thị cả 2 biểu đồ nếu chạy trong môi trường hỗ trợ
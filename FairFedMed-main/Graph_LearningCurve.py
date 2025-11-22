import matplotlib.pyplot as plt
import numpy as np

# --- 1. DỮ LIỆU TỪ TABLE I (PAPER - 2D SLO Fundus) ---
# Định dạng: 'Tên Model': [AUC, ESACC, EOD, POD/SPD]
# Lưu ý: POD ở đây dùng số liệu cột SPD (tương đương)
data_models = {
    'FedAvg':       [74.8, 67.7, 25.7, 22.7],
    'FedHEAL':      [75.9, 67.8, 24.1, 20.8],
    'PromptFL':     [73.5, 67.3, 14.9, 14.4],
    'FedOTP':       [72.3, 66.1, 13.3, 11.5],
    'FairFedLoRA':  [79.3, 73.7, 18.5, 21.7]
}

def plot_paper_comparison():
    models = list(data_models.keys())
    
    # Tách dữ liệu
    auc_vals = [data_models[m][0] for m in models]
    esacc_vals = [data_models[m][1] for m in models]
    eod_vals = [data_models[m][2] for m in models]
    spd_vals = [data_models[m][3] for m in models]

    # Cấu hình màu: FairFedLoRA màu Xanh (Nổi bật), còn lại màu Xám
    colors = ['#bdc3c7' if m != 'FairFedLoRA' else '#27ae60' for m in models]

    # Tạo layout 2x2
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # --- HÀNG 1: HIỆU SUẤT (CÀNG CAO CÀNG TỐT) ---
    
    # 1. AUC
    bars1 = axs[0, 0].bar(models, auc_vals, color=colors, width=0.6)
    axs[0, 0].set_title('AUC Score (Performance)', fontweight='bold', color='#2c3e50')
    axs[0, 0].set_ylabel('Percentage (%)')
    axs[0, 0].set_ylim(65, 85) # Zoom vào khoảng 65-85 để thấy rõ chênh lệch
    
    # 2. ESACC
    bars2 = axs[0, 1].bar(models, esacc_vals, color=colors, width=0.6)
    axs[0, 1].set_title('ESACC / ES AUC (Performance)', fontweight='bold', color='#2c3e50')
    axs[0, 1].set_ylim(60, 80)

    # --- HÀNG 2: CÔNG BẰNG (CÀNG THẤP CÀNG TỐT) ---
    
    # 3. EOD
    bars3 = axs[1, 0].bar(models, eod_vals, color=colors, width=0.6)
    axs[1, 0].set_title('EOD (Fairness Disparity)', fontweight='bold', color='#c0392b')
    axs[1, 0].set_ylabel('Disparity (%)')
    # Thêm mũi tên chỉ hướng tốt
    axs[1, 0].annotate('Thấp hơn là tốt hơn', xy=(0.5, 0.95), xycoords='axes fraction', ha='center', color='red')

    # 4. POD (SPD)
    bars4 = axs[1, 1].bar(models, spd_vals, color=colors, width=0.6)
    axs[1, 1].set_title('POD / SPD (Fairness Disparity)', fontweight='bold', color='#c0392b')
    axs[1, 1].annotate('Thấp hơn là tốt hơn', xy=(0.5, 0.95), xycoords='axes fraction', ha='center', color='red')

    # --- TRANG TRÍ CHUNG ---
    for ax in axs.flat:
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.set_xticklabels(models, rotation=15, ha='center')
        
        # Thêm số liệu lên đỉnh cột
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height}', 
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold', fontsize=9)

    plt.suptitle('So sánh các mô hình trong bài báo FairFedMed (Table I)', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig('paper_models_comparison.png')
    print("✅ Đã lưu ảnh: paper_models_comparison.png")
    plt.show()

if __name__ == "__main__":
    plot_paper_comparison()
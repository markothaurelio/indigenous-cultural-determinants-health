import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load Excel file
file_path = "ABS_Cultural_Determinants.xlsx"
df = pd.read_excel(file_path)

# Focus categories
focus_categories = [
    "Removed from natural family", "Not removed from natural family",
    "Satisfied with cultural knowledge", "Not satisfied with cultural knowledge",
    "English", "Aboriginal/Torres Strait Islander language"
]
df_focus = df[df["Category"].isin(focus_categories)].reset_index(drop=True)

# Define columns
health_cols = ["Excellent/Very Good", "Good", "Fair/Poor"]
distress_cols = ["Low/Moderate distress", "High/Very High distress"]

# Convert to percentages
health_percent = df_focus[health_cols].div(df_focus[health_cols].sum(axis=1), axis=0) * 100
distress_percent = df_focus[distress_cols].div(df_focus[distress_cols].sum(axis=1), axis=0) * 100

# Pairs for highlighting
pairs = {
    "Removal from natural family": ["Removed from natural family", "Not removed from natural family"],
    "Satisfaction with cultural knowledge": ["Satisfied with cultural knowledge", "Not satisfied with cultural knowledge"],
    "Language spoken at home": ["English", "Aboriginal/Torres Strait Islander language"]
}

def plot_highlight(pair_name, pair_categories):
    fig, axes = plt.subplots(1, 2, figsize=(20, 10), sharey=True)

    # Peach background
    fig.patch.set_facecolor("#FBE3D6")
    for ax in axes:
        ax.set_facecolor("#FBE3D6")

    # Harmonized highlight palettes
    highlight_colors_health = ["#264653", "#2A9D8F", "#E9C46A"]   # deep teal, medium teal, muted gold
    highlight_colors_distress = ["#8AB17D", "#D62828"]            # sage green, muted crimson
    grey_health = ["#E6CFCF", "#F0DCDC", "#FAEDED"]               # warm greys/pinks
    grey_distress = ["#F0DCDC", "#E6CFCF"]

    health_colors, distress_colors = [], []
    for cat in df_focus["Category"]:
        if cat in pair_categories:
            health_colors.append(highlight_colors_health)
            distress_colors.append(highlight_colors_distress)
        else:
            health_colors.append(grey_health)
            distress_colors.append(grey_distress)

    # --- Health chart ---
    for i, row in enumerate(health_percent.values):
        axes[0].barh(i, row[0], color=health_colors[i][0])
        axes[0].barh(i, row[1], left=row[0], color=health_colors[i][1])
        axes[0].barh(i, row[2], left=row[0] + row[1], color=health_colors[i][2])
        if df_focus["Category"][i] in pair_categories:
            xpos = 0
            for val in row:
                if val > 5:
                    axes[0].text(xpos + val/2, i, f"{val:.0f}%", va="center",
                                 ha="center", fontsize=11, weight="bold", color="white")
                xpos += val

    axes[0].set_title("Self-assessed Health Status (%)", fontsize=18, weight="bold", pad=30, loc="left")
    axes[0].set_yticks(range(len(df_focus)))
    axes[0].set_yticklabels(df_focus["Category"], fontsize=13)
    for label in axes[0].get_yticklabels():
        if label.get_text() in pair_categories:
            label.set_fontweight("bold")

    axes[0].set_xlabel("")
    axes[0].set_xticks([])
    axes[0].tick_params(axis="y", length=0)
    for spine in ["bottom", "top", "right", "left"]:
        axes[0].spines[spine].set_visible(False)

    # --- Distress chart ---
    for i, row in enumerate(distress_percent.values):
        axes[1].barh(i, row[0], color=distress_colors[i][0])
        axes[1].barh(i, row[1], left=row[0], color=distress_colors[i][1])
        if df_focus["Category"][i] in pair_categories:
            xpos = 0
            for val in row:
                if val > 5:
                    axes[1].text(xpos + val/2, i, f"{val:.0f}%", va="center",
                                 ha="center", fontsize=11, weight="bold", color="white")
                xpos += val

    axes[1].set_title(f"Psychological Distress (%) {pair_name}", fontsize=18, weight="bold", pad=30, loc="left")
    axes[1].set_yticks(range(len(df_focus)))
    axes[1].set_yticklabels(df_focus["Category"], fontsize=13)
    for label in axes[1].get_yticklabels():
        if label.get_text() in pair_categories:
            label.set_fontweight("bold")

    axes[1].set_xlabel("")
    axes[1].set_xticks([])
    axes[1].tick_params(axis="y", length=0)
    for spine in ["bottom", "top", "right", "left"]:
        axes[1].spines[spine].set_visible(False)

    # --- Legends ---
    health_legend = [
        Patch(facecolor=highlight_colors_health[0], label="Excellent/Very Good"),
        Patch(facecolor=highlight_colors_health[1], label="Good"),
        Patch(facecolor=highlight_colors_health[2], label="Fair/Poor")
    ]
    distress_legend = [
        Patch(facecolor=highlight_colors_distress[0], label="Low/Moderate"),
        Patch(facecolor=highlight_colors_distress[1], label="High/Very High")
    ]

    axes[0].legend(handles=health_legend, loc="upper left", bbox_to_anchor=(0, 1.02),
                   ncol=3, frameon=False)
    axes[1].legend(handles=distress_legend, loc="upper left", bbox_to_anchor=(0, 1.02),
                   ncol=2, frameon=False)

    plt.tight_layout()
    plt.show()

# Generate all three highlight charts
for name, cats in pairs.items():
    plot_highlight(name, cats)

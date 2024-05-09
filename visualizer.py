import json
import os
from collections import Counter

import matplotlib.pyplot as plt
import nltk
import numpy as np
from wordcloud import WordCloud


def vis_infos(conf_name, stopwords, num_keywords, save_dir):
    with open(f"list/{conf_name}-list.json", mode="r", encoding="utf-8") as f:
        paper_infos = json.load(f)

    keyword_list = []
    for i, paper_info in enumerate(paper_infos):
        title, authors, *links = paper_info
        # print(f"[{i}/{len(paper_infos)}] {title}")
        for word in list(set(title.lower().split(" "))):
            if word not in stopwords:
                keyword_list.append(word)

    keyword_counter = Counter(keyword_list)

    # Merge duplicates: CNNs and CNN
    print(f"[{conf_name}] {len(keyword_counter)} different keywords before merging")
    duplicates = []
    for k in keyword_counter:
        if k + "s" in keyword_counter:
            duplicates.append(k)
    for k in duplicates:
        keyword_counter[k] += keyword_counter[k + "s"]
        del keyword_counter[k + "s"]
    print(f"[{conf_name}] {len(keyword_counter)} different keywords after merging")

    # Show N most common keywords and their frequencies
    keywords_counter_vis = keyword_counter.most_common(num_keywords)

    plt.rcdefaults()
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 18))

    key = [k[0] for k in keywords_counter_vis]
    value = [k[1] for k in keywords_counter_vis]
    y_pos = np.arange(len(key))
    ax.barh(y_pos, value, align="center", color="blue", ecolor="black", log=True)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(key, rotation=0, fontsize=10)
    ax.invert_yaxis()
    for i, v in enumerate(value):
        ax.text(v + 3, i + 0.25, str(v), color="black", fontsize=10)
    ax.set_xlabel("Frequency of Top {num_keywords} Keywords")
    ax.set_title(f"Top {num_keywords} Keywords in {conf_name}")
    plt.savefig(f"{save_dir}/{conf_name}-freq.png", bbox_inches="tight", pad_inches=0, dpi=600, format="png")

    wc = WordCloud(max_font_size=64, max_words=160, width=1280, height=640, background_color="white")
    # generate word cloud
    wc.generate(" ".join(keyword_list))
    # store to file
    wc.to_file(f"{save_dir}/{conf_name}-wc.png")


def main():
    save_dir = "./vis"
    os.makedirs(save_dir, exist_ok=True)

    num_keywords = 75
    conf_names = ["CVPR2021", "CVPR2022", "CVPR2023", "CVPR2024"]
    stopwords = ["learning", "network", "neural", "networks", "deep", "via", "using", "convolutional", "single"]
    stopwords += nltk.corpus.stopwords.words("english")

    for conf_name in conf_names:
        vis_infos(conf_name, stopwords, num_keywords, save_dir)


if __name__ == "__main__":
    main()

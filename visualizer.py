import json
import os
import re
from collections import Counter, OrderedDict

import matplotlib.pyplot as plt
import nltk
import numpy as np
from wordcloud import WordCloud

RANDOM_SEED = 112358


def vis_infos(conf_name, stopwords, mergewords, num_keywords, save_dir):
    with open(f"list/{conf_name}-list.json", mode="r", encoding="utf-8") as f:
        paper_infos = json.load(f)

    keyword_list = []
    for i, paper_info in enumerate(paper_infos):
        title, authors, *links = paper_info
        for word in list(set(title.lower().split(" "))):
            if word not in stopwords:
                for k, v in mergewords.items():
                    word = re.sub(k, v, word)
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

    plt.figure(figsize=(16, 4))
    keys = [k[0] for k in keywords_counter_vis]
    values = [k[1] for k in keywords_counter_vis]
    xs = np.arange(len(keys))
    plt.bar(xs, values, width=0.6, align="center", color="blue", ecolor="black", log=True)
    plt.xlim(xs.min() - 0.5, xs.max() + 0.5)
    plt.xticks(xs, keys, rotation=90, fontsize=10)
    plt.yticks([])
    # plt.invert_xaxis()
    for i, v in enumerate(values):
        plt.text(i, v, str(v), color="black", fontsize=6, ha="center", va="bottom")
    plt.ylabel("Frequency")
    plt.title(f"Top {num_keywords} Keywords in {conf_name}")
    plt.savefig(f"{save_dir}/{conf_name}-freq.png", bbox_inches="tight", pad_inches=0, dpi=600, format="png")

    plt.figure(figsize=(16, 4))
    wc = WordCloud(
        max_font_size=64,
        max_words=160,
        width=1280,
        height=480,
        contour_color="black",
        background_color="white",
        normalize_plurals=False,
        random_state=RANDOM_SEED,
    )
    wc.generate(" ".join(keyword_list))
    plt.imshow(wc, interpolation="bilinear")
    plt.xticks([])
    plt.yticks([])
    plt.title(f"Top {num_keywords} Keywords in {conf_name}")
    plt.savefig(f"{save_dir}/{conf_name}-wc.png", bbox_inches="tight", pad_inches=0, dpi=600, format="png")


def main():
    save_dir = "./vis"
    os.makedirs(save_dir, exist_ok=True)

    num_keywords = 75
    conf_names = [
        "CVPR2021",
        "CVPR2022",
        "CVPR2023",
        "CVPR2024",
        #
        "WACV2021",
        "WACV2022",
        "WACV2023",
        "WACV2024",
        #
        "ICCV2021",
        "ICCV2023",
    ]
    mergewords = OrderedDict({r"re-identification|re-id": "re-identification"})
    stopwords = [
        "deep",
        "learning",
        "neural",
        "network",
        "networks",
        "model",
        "models",
        "convolutional",
        "via",
        "with",
        "using",
        "single",
        "object",
        "estimation",
    ]
    stopwords += nltk.corpus.stopwords.words("english")

    for conf_name in conf_names:
        vis_infos(conf_name, stopwords, mergewords, num_keywords, save_dir)


if __name__ == "__main__":
    # nltk.download("stopwords")

    main()

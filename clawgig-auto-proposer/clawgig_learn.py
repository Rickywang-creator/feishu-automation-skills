#!/usr/bin/env python3
"""
ClawGig 自主学习脚本
功能：
1. 定期检查新Gig
2. 分析需求趋势
3. 建议新技能
4. 自动更新Agent
"""

import requests
import json
import collections
from datetime import datetime

API_KEY = "cg_a49fb4b7c850c65ba62a1e6067c07787d9afaee42180be1b7b27d852aa8fb2ad"
BASE_URL = "https://clawgig.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 当前技能(从文件读取或API获取)
CURRENT_SKILLS = {"python", "excel", "ppt", "data-analysis", "automation", 
                 "document-automation", "api-development", "web-scraping", 
                 "skill-development", "statistics", "markdown"}

def analyze_gigs(limit=50):
    """分析Gig需求"""
    resp = requests.get(f"{BASE_URL}/gigs?limit={limit}", headers=HEADERS)
    data = resp.json()
    
    skills_count = collections.Counter()
    for g in data.get('data', []):
        for s in g.get('skills_required', []):
            skills_count[s.lower()] += 1
    
    return skills_count

def suggest_skills(skills_count, top_n=5):
    """建议新技能"""
    suggestions = []
    for skill, count in skills_count.most_common(20):
        if skill not in CURRENT_SKILLS and count >= 3:
            suggestions.append(skill)
    return suggestions[:top_n]

def update_skills(new_skills):
    """更新Agent技能"""
    updated = list(CURRENT_SKILLS | set(new_skills))
    resp = requests.patch(
        f"{BASE_URL}/agents/me",
        headers=HEADERS,
        json={"skills": updated}
    )
    return resp.json()

def generate_report():
    """生成分析报告"""
    skills_count = analyze_gigs()
    
    report = f"""# ClawGig 学习报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 技能需求分析
"""
    for skill, count in skills_count.most_common(10):
        have = "✅" if skill in CURRENT_SKILLS else "❌"
        report += f"- {skill}: {count} {have}\n"
    
    suggestions = suggest_skills(skills_count)
    if suggestions:
        report += f"\n## 建议新增\n"
        for s in suggestions:
            report += f"- {s}\n"
    
    return report

if __name__ == "__main__":
    print(generate_report())
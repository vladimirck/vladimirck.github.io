import json
import os
import sys

def format_score(score):
    if score is None:
        return "N/A"
    return str(int(score * 100))

def get_color(score):
    if score is None:
        return "⚪"
    if score >= 0.9:
        return "🟢"
    if score >= 0.5:
        return "🟠"
    return "🔴"

def generate_md(json_path, md_path):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    categories = data.get('categories', {})
    
    with open(md_path, 'w') as f:
        f.write("# Reporte de Lighthouse\n\n")
        f.write(f"**Fecha:** {data.get('fetchTime', 'N/A')}\n")
        f.write(f"**URL:** {data.get('finalUrl', 'N/A')}\n")
        f.write(f"**Device:** {data.get('configSettings', {}).get('formFactor', 'N/A')}\n\n")
        
        f.write("## Resumen de Puntuación\n\n")
        f.write("| Categoría | Puntuación | Estado |\n")
        f.write("| :--- | :--- | :--- |\n")
        
        for key, cat in categories.items():
            score = cat.get('score')
            f.write(f"| {cat.get('title')} | {format_score(score)} | {get_color(score)} |\n")
        
        f.write("\n## Oportunidades de Mejora (Rendimiento)\n\n")
        audits = data.get('audits', {})
        perf_audits = categories.get('performance', {}).get('auditRefs', [])
        
        # Filtrar solo las que tienen ahorro de tiempo significativo
        opportunities = []
        for ref in perf_audits:
            audit_id = ref.get('id')
            audit = audits.get(audit_id, {})
            if audit.get('details', {}).get('type') == 'opportunity':
                savings = audit.get('details', {}).get('overallSavingsMs', 0)
                if savings > 0:
                    opportunities.append((audit.get('title'), audit.get('description'), savings))
        
        opportunities.sort(key=lambda x: x[2], reverse=True)
        
        for title, desc, savings in opportunities:
            f.write(f"- **{title}**: Ahorro estimado ~{savings}ms\n")
            f.write(f"  > {desc}\n\n")

        f.write("## Principales Diagnósticos\n\n")
        diagnostic_audits = [
            'largest-contentful-paint',
            'cumulative-layout-shift',
            'total-blocking-time',
            'first-contentful-paint',
            'speed-index'
        ]
        
        for audit_id in diagnostic_audits:
            audit = audits.get(audit_id)
            if audit:
                score = audit.get('score')
                f.write(f"- **{audit.get('title')}**: {audit.get('displayValue', 'N/A')} ({get_color(score)})\n")

    print(f"Reporte Markdown generado en: {md_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python lighthouse_to_md.py <input_json> <output_md>")
    else:
        generate_md(sys.argv[1], sys.argv[2])

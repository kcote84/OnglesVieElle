import io, os, re
parts = ["part1_head.html","part2_css.html","part3_body_a.html","part4_body_b.html","part5_tail.html"]
html = ""
for f in parts:
    html += io.open(f, encoding="utf-8").read()
    if f == "part2_css.html":
        html += "</head>\n"
for tok in ["LOGO","G1","G2","G3","G4","G5","SALON"]:
    data = io.open("asset_%s.txt"%tok, encoding="utf-8").read().strip()
    html = html.replace("{{%s}}"%tok, data)
left = re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
assert not left, left
out = r"G:/Mon disque/Dactyl/SITE WEB CLIENTS/Ongles Vie-Elle/index.html"
io.open(out,"w",encoding="utf-8",newline="\n").write(html)
print("OK", len(html)//1024, "KB")

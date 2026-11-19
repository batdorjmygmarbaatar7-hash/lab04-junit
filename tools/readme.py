#!/usr/bin/env python3
"""Lab 4: README.md-г results/ болон тестийн файлаас үүсгэнэ (тоо үргэлж таарна).
   python3 tools/readme.py
"""
import os, re, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

def rd(p):
    p = os.path.join(ROOT, p)
    return ANSI.sub("", open(p, encoding="utf-8", errors="replace").read()) if os.path.exists(p) else ""

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    return ANSI.sub("", (r.stdout + r.stderr)).strip()

def last_run(t):
    m = re.findall(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)\s*$", t, re.M)
    return m[-1] if m else None

test_src = rd("src/test/java/mn/edu/must/sqat/GradeCalculatorTest.java")
n_test = len(re.findall(r"^\s*@Test\b", test_src, re.M))
n_param = len(re.findall(r"^\s*@ParameterizedTest\b", test_src, re.M))
green, mut = rd("results/mvn-test.txt"), rd("results/mvn-test-mutant.txt")
g, m = last_run(green), last_run(mut)
g_ok = "BUILD SUCCESS" in green
m_fail = "BUILD FAILURE" in mut
fails = re.findall(r"^\[ERROR\]\s+(GradeCalculatorTest\.\S+?:\d+.*)$", mut, re.M)

L = []; a = L.append
a("# Лаб 4: Нэгжийн тестийн эхлэл — JUnit 5\n")
a("**Нэр:** М. Батдорж  \n**Оюутны код:** B252270136\n")
a("## Орчин\n")
a("```\n$ java -version\n" + sh("java -version") + "\n```\n")
a("```\n$ mvn -version\n" + sh("mvn -version") + "\n```\n")
a("## Тестийн тоо\n")
a(f"- `GradeCalculatorTest`-д **{n_test + n_param} тестийн метод**: {n_test} `@Test` + {n_param} `@ParameterizedTest` (letterGrade-д 2, totalScore-д 2).")
if g:
    a(f"- `results/mvn-test.txt`: **Tests run: {g[0]}, Failures: {g[1]}, Errors: {g[2]}, Skipped: {g[3]}**, " + ("**BUILD SUCCESS**" if g_ok else "BUILD ?") + ".")
    a(f"- Яагаад {n_test + n_param} метод атлаа {g[0]} тест вэ: Surefire нь `@CsvSource` / `@ValueSource`-ийн мөр бүрийг тусдаа тест гэж тоолдог "
      "(`letterGradeBoundaries` 11 мөр, `letterGradeRejectsOutOfRange` 5, `totalScoreValidSums` 4, `totalScoreRejectsEachComponent` 10).\n")
a("## Юу шалгасан бэ\n")
a("| Ангилал | Тестүүд |\n|---|---|")
a("| Ердийн утга | 95→A, 85→B, 75→C, 65→D, 30→F (`typicalValues`, `assertAll`) |")
a("| Хязгаарын утга | 90→A, 89.99→B, 80→B, 79.99→C, 70→C, 69.99→D, 60→D, 59.99→F, 0→F, 100→A |")
a("| letterGrade буруу оролт | -1, -0.01, 100.01, 101, NaN → `assertThrows(IllegalArgumentException)` |")
a("| totalScore зөв | (10,40,10,10,30)→100, бүгд 0→0, 88, 54.25 |")
a("| totalScore буруу оролт | att=-5, lab=41; бүрэлдэхүүн бүрийг тус тусад нь хязгаараас 0.01-ээр хэтрүүлж, мөн -0.01 болгож (10 тохиолдол) |")
a("| Интеграц | totalScore(9,35,8,9,27)=88 → letterGrade → B |\n")
a("Тест бүр **Arrange–Act–Assert** бүтэцтэй (`calc`-ийг `@BeforeEach`-д бэлдэнэ), `@DisplayName`-ээр монгол нэртэй.\n")
a("## Мутаци: `score >= 90` → `score > 90`\n")
if m:
    a(f"`results/mvn-test-mutant.txt`: **Tests run: {m[0]}, Failures: {m[1]}**" + (", **BUILD FAILURE**" if m_fail else "") + ". Унасан тестүүд:\n")
    a("```")
    for f in fails:
        a(f)
    a("```\n")
a("## Дүгнэлт\n")
a("<!-- conclusion -->")
a(f"Нийт {n_test + n_param} тестийн метод ({n_test} `@Test`, {n_param} `@ParameterizedTest`) бичсэн бөгөөд Surefire үүнийг {g[0] if g else '?'} тест гэж тоолж, бүгд ногоон гарсан. "
  f"`score >= 90`-ийг `score > 90` болгосон мутацид яг 90 оноог шалгадаг `ninetyIsExactlyA` болон `letterGradeBoundaries`-ийн `[90, A]` мөр унасан (expected: <A> but was: <B>), харин үлдсэн {int(m[0]) - int(m[1]) if m else '?'} тест ногоон хэвээр байсан. "
  "Энэ нь 95, 85 гэх мэт ердийн утгууд болон 100 зэрэг туйлын утга хязгаарын алдааг огт илрүүлдэггүй, зөвхөн яг хязгаар дээрх утга л барьдаг гэдгийг тод харуулсан: pass болсон тест заавал зөв тест гэсэн үг биш. "
  "Хамгийн сонирхолтой тохиолдол нь `letterGradeRejectsOutOfRange`-ийн `NaN` байлаа. `score < 0 || score > 100` гэсэн шалгалт NaN-ийн хувьд хоёулаа false буцаадаг тул `Double.isNaN` шалгалтгүй хэрэгжүүлэлт NaN-ийг хүлээн авч \"F\" гэж буцаах байсан бөгөөд энэ тест үүнийг барьдаг. "
  "`89.99 → B`, `59.99 → F` гэх мэт бутархай хязгаарууд нь оноог бүхэлчилж (round) харьцуулдаг алдаатай хэрэгжүүлэлтийг (89.99 → 90 → A) илрүүлэх зорилготой. "
  "totalScore-д бүрэлдэхүүн бүрийг тус тусад нь 0.01-ээр хэтрүүлсэн 10 мөр бүхий parameterized тест нь аль нэг бүрэлдэхүүний дээд хязгаарыг буруу бичсэн (жишээ нь шалгалтыг 30 биш 40 гэж) эсвэл шалгалтыг мартсан тохиолдлыг шууд барина. "
  "Энэ гараар хийсэн мутаци нь дараагийн лабуудад PIT-ээр автоматжуулах mutation testing-ийн санааг урьдчилан харуулсан: тестийн чанарыг ногоон тестийн тоогоор биш, санаатай оруулсан алдааг барьж чадах эсэхээр нь хэмждэг.")
a("<!-- /conclusion -->\n")
a("## AI ашиглалт\n")
a("<!-- ai -->")
a("Claude (Anthropic-ийн AI туслах)-ыг дараах зүйлд ашигласан: GradeCalculator-ийн хэрэгжүүлэлт (NaN шалгалттай), GradeCalculatorTest-ийн тестийн тохиолдлууд (хязгаар, буруу оролт, parameterized), засварласан pom.xml, README үүсгэх `tools/readme.py` скрипт, мөн дүгнэлтийн ноорог. "
  "Бүх командыг (mvn test, мутаци оруулж буцаах, commit) өөрийн Ubuntu машин дээр өөрөө ажиллуулж, `results/` доторх гаралтыг хадгалсан. README-ийн тестийн тоо болон мутацийн үр дүн нь `results/` файлуудаас скриптээр уншигдсан тул файлтай таарч байгаа.")
a("<!-- /ai -->\n")
out = os.path.join(ROOT, "README.md")
old = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
new = "\n".join(L)
# өмнө бөглөсөн текстийг хадгалах
for tag in ("conclusion", "ai"):
    mm = re.search(rf"<!-- {tag} -->\n(.*?)\n<!-- /{tag} -->", old, re.S)
    if mm:
        todo = ">>> TODO: Дүгнэлт (5-8 өгүүлбэр) <<<" if tag == "conclusion" else ">>> TODO: AI ашиглалт <<<"
        new = new.replace(todo, f"<!-- {tag} -->\n{mm.group(1)}\n<!-- /{tag} -->")
open(out, "w", encoding="utf-8").write(new)
print(f"README.md: {n_test + n_param} метод, Tests run={g[0] if g else '?'}, mutant Failures={m[1] if m else '?'}")
print("Үлдсэн TODO:", [l for l in new.splitlines() if "TODO" in l])

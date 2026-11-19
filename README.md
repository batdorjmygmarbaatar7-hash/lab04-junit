# Лаб 4: Нэгжийн тестийн эхлэл — JUnit 5

**Нэр:** М. Батдорж  
**Оюутны код:** B252270136

## Орчин

```
$ java -version
openjdk version "17.0.21.0.3" 2026-10-24
OpenJDK Runtime Environment (build 17.0.21.0.3+1-1-26.04.1-Ubuntu)
OpenJDK 64-Bit Server VM (build 17.0.21.0.3+1-1-26.04.1-Ubuntu, mixed mode, sharing)
```

```
$ mvn -version
Apache Maven 3.9.12
Maven home: /usr/share/maven
Java version: 17.0.21.0.3, vendor: Ubuntu, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "7.0.0-43-generic", arch: "amd64", family: "unix"
```

## Тестийн тоо

- `GradeCalculatorTest`-д **15 тестийн метод**: 11 `@Test` + 4 `@ParameterizedTest` (letterGrade-д 2, totalScore-д 2).
- `results/mvn-test.txt`: **Tests run: 41, Failures: 0, Errors: 0, Skipped: 0**, **BUILD SUCCESS**.
- Яагаад 15 метод атлаа 41 тест вэ: Surefire нь `@CsvSource` / `@ValueSource`-ийн мөр бүрийг тусдаа тест гэж тоолдог (`letterGradeBoundaries` 11 мөр, `letterGradeRejectsOutOfRange` 5, `totalScoreValidSums` 4, `totalScoreRejectsEachComponent` 10).

## Юу шалгасан бэ

| Ангилал | Тестүүд |
|---|---|
| Ердийн утга | 95→A, 85→B, 75→C, 65→D, 30→F (`typicalValues`, `assertAll`) |
| Хязгаарын утга | 90→A, 89.99→B, 80→B, 79.99→C, 70→C, 69.99→D, 60→D, 59.99→F, 0→F, 100→A |
| letterGrade буруу оролт | -1, -0.01, 100.01, 101, NaN → `assertThrows(IllegalArgumentException)` |
| totalScore зөв | (10,40,10,10,30)→100, бүгд 0→0, 88, 54.25 |
| totalScore буруу оролт | att=-5, lab=41; бүрэлдэхүүн бүрийг тус тусад нь хязгаараас 0.01-ээр хэтрүүлж, мөн -0.01 болгож (10 тохиолдол) |
| Интеграц | totalScore(9,35,8,9,27)=88 → letterGrade → B |

Тест бүр **Arrange–Act–Assert** бүтэцтэй (`calc`-ийг `@BeforeEach`-д бэлдэнэ), `@DisplayName`-ээр монгол нэртэй.

## Мутаци: `score >= 90` → `score > 90`

`results/mvn-test-mutant.txt`: **Tests run: 41, Failures: 2**, **BUILD FAILURE**. Унасан тестүүд:

```
GradeCalculatorTest.letterGradeBoundaries:150 expected: <A> but was: <B>
GradeCalculatorTest.ninetyIsExactlyA:46 expected: <A> but was: <B>
```

## Дүгнэлт

<!-- conclusion -->
Нийт 15 тестийн метод (11 `@Test`, 4 `@ParameterizedTest`) бичсэн бөгөөд Surefire үүнийг 41 тест гэж тоолж, бүгд ногоон гарсан. `score >= 90`-ийг `score > 90` болгосон мутацид яг 90 оноог шалгадаг `ninetyIsExactlyA` болон `letterGradeBoundaries`-ийн `[90, A]` мөр унасан (expected: <A> but was: <B>), харин үлдсэн 39 тест ногоон хэвээр байсан. Энэ нь 95, 85 гэх мэт ердийн утгууд болон 100 зэрэг туйлын утга хязгаарын алдааг огт илрүүлдэггүй, зөвхөн яг хязгаар дээрх утга л барьдаг гэдгийг тод харуулсан: pass болсон тест заавал зөв тест гэсэн үг биш. Хамгийн сонирхолтой тохиолдол нь `letterGradeRejectsOutOfRange`-ийн `NaN` байлаа. `score < 0 || score > 100` гэсэн шалгалт NaN-ийн хувьд хоёулаа false буцаадаг тул `Double.isNaN` шалгалтгүй хэрэгжүүлэлт NaN-ийг хүлээн авч "F" гэж буцаах байсан бөгөөд энэ тест үүнийг барьдаг. `89.99 → B`, `59.99 → F` гэх мэт бутархай хязгаарууд нь оноог бүхэлчилж (round) харьцуулдаг алдаатай хэрэгжүүлэлтийг (89.99 → 90 → A) илрүүлэх зорилготой. totalScore-д бүрэлдэхүүн бүрийг тус тусад нь 0.01-ээр хэтрүүлсэн 10 мөр бүхий parameterized тест нь аль нэг бүрэлдэхүүний дээд хязгаарыг буруу бичсэн (жишээ нь шалгалтыг 30 биш 40 гэж) эсвэл шалгалтыг мартсан тохиолдлыг шууд барина. Энэ гараар хийсэн мутаци нь дараагийн лабуудад PIT-ээр автоматжуулах mutation testing-ийн санааг урьдчилан харуулсан: тестийн чанарыг ногоон тестийн тоогоор биш, санаатай оруулсан алдааг барьж чадах эсэхээр нь хэмждэг.
<!-- /conclusion -->

## AI ашиглалт

<!-- ai -->
Claude (Anthropic-ийн AI туслах)-ыг дараах зүйлд ашигласан: GradeCalculator-ийн хэрэгжүүлэлт (NaN шалгалттай), GradeCalculatorTest-ийн тестийн тохиолдлууд (хязгаар, буруу оролт, parameterized), засварласан pom.xml, README үүсгэх `tools/readme.py` скрипт, мөн дүгнэлтийн ноорог. Бүх командыг (mvn test, мутаци оруулж буцаах, commit) өөрийн Ubuntu машин дээр өөрөө ажиллуулж, `results/` доторх гаралтыг хадгалсан. README-ийн тестийн тоо болон мутацийн үр дүн нь `results/` файлуудаас скриптээр уншигдсан тул файлтай таарч байгаа.
<!-- /ai -->

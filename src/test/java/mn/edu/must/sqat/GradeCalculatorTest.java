package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

/** GradeCalculator-ийн нэгжийн тестүүд (JUnit 5, AAA бүтэц). */
class GradeCalculatorTest {

    private GradeCalculator calc;

    @BeforeEach
    void setUp() {
        calc = new GradeCalculator(); // Arrange (бүх тестэд нийтлэг)
    }

    // ---------- letterGrade: ердийн утгууд ----------

    @Test
    @DisplayName("Ердийн утгууд: 95→A, 85→B, 75→C, 65→D, 30→F")
    void typicalValues() {
        // Arrange: calc (setUp) | Act + Assert: бүгдийг нэг дор шалгана
        assertAll(
                () -> assertEquals("A", calc.letterGrade(95)),
                () -> assertEquals("B", calc.letterGrade(85)),
                () -> assertEquals("C", calc.letterGrade(75)),
                () -> assertEquals("D", calc.letterGrade(65)),
                () -> assertEquals("F", calc.letterGrade(30)));
    }

    // ---------- letterGrade: хязгаарын утгууд ----------

    @Test
    @DisplayName("90 оноо яг A дүн байх ёстой (хязгаарын тохиолдол)")
    void ninetyIsExactlyA() {
        double score = 90.0;                    // Arrange
        String grade = calc.letterGrade(score); // Act
        assertEquals("A", grade);               // Assert
    }

    @Test
    @DisplayName("89.99 оноо B дүн (A-гийн хязгаараас яг доор)")
    void justBelowNinetyIsB() {
        double score = 89.99;                   // Arrange
        String grade = calc.letterGrade(score); // Act
        assertEquals("B", grade);               // Assert
    }

    @Test
    @DisplayName("60 оноо D, 59.99 оноо F (тэнцэх хязгаар)")
    void passingBoundarySixty() {
        // Arrange
        double atLimit = 60.0;
        double belowLimit = 59.99;
        // Act
        String atGrade = calc.letterGrade(atLimit);
        String belowGrade = calc.letterGrade(belowLimit);
        // Assert
        assertAll(
                () -> assertEquals("D", atGrade),
                () -> assertEquals("F", belowGrade));
    }

    @Test
    @DisplayName("Хүчинтэй мужийн туйлууд: 0 → F, 100 → A")
    void extremesZeroAndHundred() {
        // Act
        String low = calc.letterGrade(0);
        String high = calc.letterGrade(100);
        // Assert
        assertAll(
                () -> assertEquals("F", low),
                () -> assertEquals("A", high));
    }

    // ---------- letterGrade: буруу оролт ----------

    @Test
    @DisplayName("-1 оноо IllegalArgumentException шиднэ")
    void letterGradeRejectsNegative() {
        double score = -1;                                   // Arrange
        assertThrows(IllegalArgumentException.class,         // Act + Assert
                () -> calc.letterGrade(score));
    }

    @Test
    @DisplayName("101 оноо IllegalArgumentException шиднэ")
    void letterGradeRejectsOver100() {
        double score = 101;                                  // Arrange
        assertThrows(IllegalArgumentException.class,         // Act + Assert
                () -> calc.letterGrade(score));
    }

    // ---------- totalScore ----------

    @Test
    @DisplayName("Бүх бүрэлдэхүүн дээд оноотой (10, 40, 10, 10, 30) бол нийлбэр 100")
    void totalScoreMaxIs100() {
        // Act
        double total = calc.totalScore(10, 40, 10, 10, 30);
        // Assert
        assertEquals(100.0, total, 1e-9);
    }

    @Test
    @DisplayName("Ирц сөрөг (-5) бол totalScore exception шиднэ")
    void totalScoreRejectsNegative() {
        double att = -5;                                                 // Arrange
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> calc.totalScore(att, 30, 8, 8, 20));               // Act
        assertTrue(ex.getMessage().contains("ирц"));                     // Assert: аль бүрэлдэхүүн буруу вэ
    }

    @Test
    @DisplayName("Лаб+бие даалт 41 (дээд хязгаар 40-өөс хэтэрсэн) бол exception шиднэ")
    void totalScoreRejectsOverMax() {
        double lab = 41;                                                 // Arrange
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> calc.totalScore(10, lab, 10, 10, 30));             // Act
        assertTrue(ex.getMessage().contains("лаб"));                     // Assert
    }

    @Test
    @DisplayName("Нийлбэр → үсгэн дүн: 9+35+8+9+27 = 88 → B")
    void totalScoreThenLetterGrade() {
        // Act
        double total = calc.totalScore(9, 35, 8, 9, 27);
        String grade = calc.letterGrade(total);
        // Assert
        assertAll(
                () -> assertEquals(88.0, total, 1e-9),
                () -> assertEquals("B", grade));
    }

    // ---------- Parameterized тестүүд ----------

    @ParameterizedTest(name = "{0} оноо → {1}")
    @DisplayName("letterGrade-ийн бүх хязгаар (parameterized)")
    @CsvSource({"95,A", "90,A", "89.99,B", "80,B", "79.99,C", "70,C",
                "69.99,D", "60,D", "59.99,F", "0,F", "100,A"})
    void letterGradeBoundaries(double score, String expected) {
        assertEquals(expected, calc.letterGrade(score));
    }

    @ParameterizedTest(name = "{0} оноо → exception")
    @DisplayName("letterGrade: 0-100-аас гадуурх болон NaN утга exception шиднэ (parameterized)")
    @ValueSource(doubles = {-1, -0.01, 100.01, 101, Double.NaN})
    void letterGradeRejectsOutOfRange(double score) {
        assertThrows(IllegalArgumentException.class, () -> calc.letterGrade(score));
    }

    @ParameterizedTest(name = "{0}+{1}+{2}+{3}+{4} = {5}")
    @DisplayName("totalScore: хүчинтэй утгуудын нийлбэр (parameterized)")
    @CsvSource({"10,40,10,10,30,100", "0,0,0,0,0,0", "9,35,8,9,27,88", "5.5,20.25,7,6.5,15,54.25"})
    void totalScoreValidSums(double att, double lab, double q1, double q2, double exam, double expected) {
        assertEquals(expected, calc.totalScore(att, lab, q1, q2, exam), 1e-9);
    }

    @ParameterizedTest(name = "({0}, {1}, {2}, {3}, {4}) → exception")
    @DisplayName("totalScore: бүрэлдэхүүн бүрийн хязгаараас хэтэрсэн болон сөрөг утга (parameterized)")
    @CsvSource({"10.01,0,0,0,0", "0,40.01,0,0,0", "0,0,10.01,0,0", "0,0,0,10.01,0", "0,0,0,0,30.01",
                "-0.01,0,0,0,0", "0,-0.01,0,0,0", "0,0,-0.01,0,0", "0,0,0,-0.01,0", "0,0,0,0,-0.01"})
    void totalScoreRejectsEachComponent(double att, double lab, double q1, double q2, double exam) {
        assertThrows(IllegalArgumentException.class, () -> calc.totalScore(att, lab, q1, q2, exam));
    }
}

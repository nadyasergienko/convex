from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь нульугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))
        Figure.fixed_point = R2Point(1.0, 1.0)

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        assert self.f.perimeter() == 0.0

    # Площадь одноугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)

    def test_g(self):
        assert self.f.g() == 1


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        assert self.f.perimeter() == approx(2.0)

    # Площадь двуугольника нулевая
    def test_аrea(self):
        assert self.f.area() == 0.0

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # При добавлении точки двуугольник может превратиться в другой двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)

    def test_g1(self):
        t = Segment(R2Point(0.5, 0.5), R2Point(2.0, 2.0))
        assert t.g() == 2

    # Функция `g` вычисляется корректно
    def test_g2(self):
        t = Segment(R2Point(-2.0, 0.0), R2Point(5.0, 0.0))
        assert t.g() == 0


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Polygon(
            R2Point(
                0.0, 0.0), R2Point(
                1.0, 0.0), R2Point(
                0.0, 1.0))

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon(self):
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3
    #   добавление точки внутрь многоугольника не меняет их количества

    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3
    #   добавление другой точки может изменить их количество

    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4
    #   изменения выпуклой оболочки могут и уменьшать их количество

    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter1(self):
        assert self.f.perimeter() == approx(2.0 + sqrt(2.0))
    #   добавление точки может его изменить

    def test_perimeter2(self):
        assert self.f.add(R2Point(1.0, 1.0)).perimeter() == approx(4.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_аrea1(self):
        assert self.f.area() == approx(0.5)
    #   добавление точки может увеличить площадь

    def test_area2(self):
        assert self.f.add(R2Point(1.0, 1.0)).area() == approx(1.0)

    def test_g1(self):
        t = Segment(R2Point(1.5, 3.0), R2Point(0.0, 0.0))
        t = t.add(R2Point(6.0, -2.0))
        assert t.g() == 2

    def test_g2(self):
        t = Segment(R2Point(4.0, 3.0), R2Point(7.0, 3.0))
        t = t.add(R2Point(4.0, 0.0))
        t = t.add(R2Point(7.0, 0.0))
        assert t.g() == 2

    def test_g3(self):
        t = Segment(R2Point(0.0, 0.0), R2Point(1.0, 5.0))
        t = t.add(R2Point(5.0, 5.0))
        t = t.add(R2Point(3.0, 0.0))
        t = t.add(R2Point(5.0, 0.0))
        assert t.g() == 1

    def test_g4(self):
        t = Segment(R2Point(0.0, 1.5), R2Point(-2.0, 5.0))
        t = t.add(R2Point(6.0, 5.0))
        t = t.add(R2Point(3.0, 1.5))
        t = t.add(R2Point(6.0, 0.0))
        t = t.add(R2Point(-2.0, 0.0))
        assert t.g() == 0

    def test_g5(self):
        t = Segment(R2Point(-2.0, 0.0), R2Point(-0.8, 1.2))
        t = t.add(R2Point(-1.0, 4.0))
        t = t.add(R2Point(1.5, 1.5))
        t = t.add(R2Point(4.0, 4.0))
        t = t.add(R2Point(5.0, 0.0))
        assert t.g() == 0

    def test_g6(self):
        t = Segment(R2Point(1.0, 2.0), R2Point(1.0, 1.0))
        t = t.add(R2Point(2.0, 1.0))
        t = t.add(R2Point(3.0, 0.0))
        t = t.add(R2Point(0.0, 0.0))
        t = t.add(R2Point(0.0, 3.0))
        t = t.add(R2Point(-1.0, 4.0))
        t = t.add(R2Point(4.0, -1.0))
        assert t.g() == 1

    def test_g7(self):
        t = Segment(R2Point(0.0, 1.0), R2Point(1.0, 1.0))
        t = t.add(R2Point(1.0, 0.0))
        t = t.add(R2Point(3.0, 2.0))
        t = t.add(R2Point(2.1, 2.1))
        t = t.add(R2Point(2.0, 3.0))
        t = t.add(R2Point(-2.0, 5.0))
        t = t.add(R2Point(5.0, -2.0))
        assert t.g() == 4

    def test_g8(self):
        t = Segment(R2Point(0.0, 7.0), R2Point(5.0, 2.0))
        t = t.add(R2Point(-9.0, -5.0))
        t = t.add(R2Point(3.0, -4.0))
        t = t.add(R2Point(3.1, 2.0))
        t = t.add(R2Point(15.0, 8.0))
        t = t.add(R2Point(132.0, 225.0))
        t = t.add(R2Point(-50.0, 78.0))
        assert t.g() == 0

    def test_g9(self):
        t = Segment(R2Point(1.2, 0.8), R2Point(3.3, 1.5))
        t = t.add(R2Point(2.9, 1.9))
        t = t.add(R2Point(0.6, 2.5))
        t = t.add(R2Point(0.33, 0.45))
        t = t.add(R2Point(2.6, 0.25))
        t = t.add(R2Point(2.3, 2.6))
        assert t.g() == 5

    def test_g10(self):
        t = Segment(R2Point(0.8, 1.3), R2Point(4.0, 5.0))
        t = t.add(R2Point(3.0, 2.1))
        t = t.add(R2Point(-0.6, 5.0))
        t = t.add(R2Point(-1.5, -3.0))
        t = t.add(R2Point(1.5, 0.0))
        t = t.add(R2Point(1.6, -0.1))
        t = t.add(R2Point(1.82, -0.55))
        t = t.add(R2Point(2.0, 1.3))
        t = t.add(R2Point(2.0, 0.5))
        t = t.add(R2Point(2.5, 0.1))
        t = t.add(R2Point(-3.0, 5.0))
        assert t.g() == 2

    def test_g11(self):
        t = Segment(R2Point(1.5, 1.5), R2Point(1.8, 1.0))
        t = t.add(R2Point(2.0, 1.5))
        t = t.add(R2Point(1.3, 1.4))
        t = t.add(R2Point(1.9, 2.0))
        t = t.add(R2Point(0.1, 0.8))
        t = t.add(R2Point(0.2, 0.3))
        t = t.add(R2Point(0.5, 0.5))
        t = t.add(R2Point(3.6, 1.2))
        t = t.add(R2Point(2.9, 4.0))
        t = t.add(R2Point(1.5, -0.2))
        t = t.add(R2Point(-0.8, 2.5))
        t = t.add(R2Point(0, 4.0))
        assert t.g() == 6

    def test_g12(self):
        t = Segment(R2Point(13.0, 13.0), R2Point(0.0, 5.0))
        t = t.add(R2Point(-5.0, -5.0))
        t = t.add(R2Point(0.0, -0.2))
        t = t.add(R2Point(1.0, 1.0))
        t = t.add(R2Point(1.2, 1.3))
        t = t.add(R2Point(2.5, 1.5))
        t = t.add(R2Point(2.0, -1.0))
        t = t.add(R2Point(3.0, 0.0))
        t = t.add(R2Point(-5.0, 0.0))
        t = t.add(R2Point(-2.5, 8.0))
        assert t.g() == 2

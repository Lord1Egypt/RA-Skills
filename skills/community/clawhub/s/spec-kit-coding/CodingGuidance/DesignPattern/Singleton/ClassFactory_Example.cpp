/**
 * @file    ClassFactory_Example.cpp
 * @brief   Usage example and self-test for the ClassFactory.
 *
 * @details
 * Build (Linux):
 *   g++ -std=c++17 -I. ClassFactory_Example.cpp -o ClassFactory_Example
 *
 * Build (Windows / MSVC):
 *   cl /std:c++17 /I. ClassFactory_Example.cpp /Fe:ClassFactory_Example.exe
 *
 * Header-only library; no additional source files to link.
 */

#include "ClassFactory.hpp"
#include <iostream>
#include <cassert>
#include <string>
#include <vector>

/* ================================================================ */
/*  1. Define a base class and several derived classes               */
/* ================================================================ */

class Shape {
public:
    virtual ~Shape() = default;
    virtual std::string name() const = 0;
    virtual double area() const = 0;
};

class Circle : public Shape {
public:
    std::string name() const override { return "Circle"; }
    double area() const override { return 3.14159 * 5 * 5; }
};

class Rectangle : public Shape {
public:
    std::string name() const override { return "Rectangle"; }
    double area() const override { return 10.0 * 20.0; }
};

class Triangle : public Shape {
public:
    std::string name() const override { return "Triangle"; }
    double area() const override { return 0.5 * 8.0 * 6.0; }
};

/* ================================================================ */
/*  2. Compile-time auto-registration (runs before main)            */
/* ================================================================ */

REGISTER_CLASS(Circle);
REGISTER_CLASS(Rectangle);
REGISTER_CLASS(Triangle);

/* ================================================================ */
/*  3. Run-time creation by name                                    */
/* ================================================================ */

int main()
{
    auto& factory = ClassFactory::instance();

    /* List all registered classes. */
    std::cout << "=== Registered classes ===" << std::endl;
    for (auto& n : factory.registeredNames()) {
        std::cout << "  " << n << std::endl;
    }
    assert(factory.size() == 3);

    /* Query. */
    assert(factory.has("Circle"));
    assert(factory.has("Rectangle"));
    assert(factory.has("Triangle"));
    assert(!factory.has("Hexagon"));

    /* Type-safe creation (returns unique_ptr<Shape>). */
    auto circle = factory.create<Shape>("Circle");
    assert(circle != nullptr);
    std::cout << "\nCreated: " << circle->name()
              << ", area = " << circle->area() << std::endl;

    auto rect = factory.create<Shape>("Rectangle");
    assert(rect != nullptr);
    std::cout << "Created: " << rect->name()
              << ", area = " << rect->area() << std::endl;

    auto tri = factory.create<Shape>("Triangle");
    assert(tri != nullptr);
    std::cout << "Created: " << tri->name()
              << ", area = " << tri->area() << std::endl;

    /* Unknown class -> nullptr. */
    auto unknown = factory.create<Shape>("Hexagon");
    assert(unknown == nullptr);
    std::cout << "\n'Hexagon' not registered, got nullptr. OK." << std::endl;

    /* Config-driven creation: simulate reading class names from a file. */
    std::cout << "\n=== Config-driven creation ===" << std::endl;
    std::vector<std::string> configShapes = {
        "Circle", "Triangle", "Rectangle", "Circle"
    };
    for (auto& shapeName : configShapes) {
        auto shape = factory.create<Shape>(shapeName);
        if (shape) {
            std::cout << "  " << shape->name()
                      << " -> area = " << shape->area() << std::endl;
        }
    }

    std::cout << "\nAll tests passed!" << std::endl;
    return 0;
}

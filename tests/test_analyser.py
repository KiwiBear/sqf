from unittest import TestCase

from sqf.parser import parse
from sqf.analyser import analyze


class AnalyseTestCase(TestCase):

    def test_statement(self):
        code = '_x=2 _y=3;'
        result = parse(code)

        errors = analyze(result)

        self.assertEqual(len(errors), 1)
        self.assertEqual((1, 6), errors[0].position)

    def test_code(self):
        code = "x = {\n    call {_x=1 _y = 2;}\n}"
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 1)
        self.assertEqual((2, 16), errors[0].position)

    def test_code1(self):
        code = "_damage = 0\nif (not _onoff) then {_damage = 0.95;};"
        result = parse(code)
        errors = analyze(result)
        self.assertEqual(len(errors), 1)
        self.assertEqual((2, 1), errors[0].position)

    def test_private1(self):
        code = "private _posicion = _location call AS_fnc_location_position;"
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_foreach(self):
        code = "{sleep 1} forEach _lamps;"
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_getConfig(self):
        code = 'configFile >> "CfgWeapons" >> _name >> "WeaponSlotsInfo" >> "mass"'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_lowercase(self):
        code = 'mapa = "MapBoard_altis_F" createvehicle [0,0,0];'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_define_simple(self):
        code = "#define CHECK_CATEGORY 2\n"
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_define_error(self):
        code = "#define\n"
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 1)
        self.assertEqual((1, 1), errors[0].position)

    def test_define(self):
        code = '#define CHECK_CATEGORY(_category) (if !(_category in AS_AAFarsenal_categories) then { \\\n' \
               '\tdiag_log format ["[AS] AS_AAFarsenal: category %1 does not exist.", _category];} \\\n    );\n'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_include(self):
        code = '#include "macros.hpp"\n_x = 1;'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 0)

    def test_include_error(self):
        code = '#include _x\n'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 1)
        self.assertEqual((1, 1), errors[0].position)

    def test_include_error_len(self):
        code = '#include\n'
        errors = analyze(parse(code))
        self.assertEqual(len(errors), 1)
        self.assertEqual((1, 1), errors[0].position)
from converters.calibre_convert import CalibreConverter


def test_convert_uses_calibre_for_kepub_output(monkeypatch, safe_path_test_settings):
    input_name = "a" * 32
    input_file = safe_path_test_settings.upload_dir / f"{input_name}.epub"
    input_file.write_text("epub fixture")

    output_file = safe_path_test_settings.output_dir / f"{input_name}.kepub.epub"
    calls: list[list[str]] = []

    def fake_run(cmd, capture_output, text, check, timeout):
        calls.append(cmd)
        output_file.write_text("kepub output")

        class Result:
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr("converters.calibre_convert.subprocess.run", fake_run)

    converter = CalibreConverter(
        input_file=str(input_file),
        output_dir=str(safe_path_test_settings.output_dir),
        input_type="epub",
        output_type="kepub",
    )

    assert converter.convert() == [str(output_file)]
    assert calls == [[
        converter.calibre_path,
        str(input_file),
        str(output_file),
    ]]


def test_convert_stages_kepub_input_as_epub(monkeypatch, safe_path_test_settings):
    input_name = "b" * 32
    input_file = safe_path_test_settings.upload_dir / f"{input_name}.kepub.epub"
    input_file.write_text("kepub fixture")

    output_file = safe_path_test_settings.output_dir / f"{input_name}.mobi"
    calls: list[list[str]] = []

    def fake_run(cmd, capture_output, text, check, timeout):
        calls.append(cmd)
        output_file.write_text("mobi output")

        class Result:
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr("converters.calibre_convert.subprocess.run", fake_run)

    converter = CalibreConverter(
        input_file=str(input_file),
        output_dir=str(safe_path_test_settings.output_dir),
        input_type="kepub",
        output_type="mobi",
    )

    assert converter.convert() == [str(output_file)]
    assert len(calls) == 1
    assert calls[0][0] == converter.calibre_path
    assert calls[0][2] == str(output_file)
    assert calls[0][1].endswith('.epub')
    assert calls[0][1] != str(input_file)


def test_can_register_uses_calibre_binary(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd, check, stdout, stderr):
        calls.append(cmd)

    monkeypatch.setattr("converters.calibre_convert.subprocess.run", fake_run)

    assert CalibreConverter.can_register() is True
    assert calls == [[CalibreConverter.calibre_path, "--version"]]
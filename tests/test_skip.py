"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
"""
import pytest
from selene import browser, have
from selenium.webdriver.chrome.options import Options

@pytest.fixture(params=['1920,1080', '375,667'])
def setup_browser(request):
    options = Options()
    current_resolution = request.param
    options.add_argument(f"window-size={current_resolution}")
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

    yield current_resolution

    browser.quit()

def test_github_desktop(setup_browser):
    if setup_browser not in ['1920,1080']:
        pytest.skip(reason='desktop only')
    browser.open('/')

    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))

def test_github_mobile(setup_browser):
    if setup_browser not in ['375,667']:
        pytest.skip(reason='only for mobile versions')
    browser.open('/')

    browser.element('.Button--link').click()
    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))
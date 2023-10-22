import pytest
from selene import browser, have
from selenium.webdriver.chrome.options import Options


"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""
@pytest.fixture(
    params=['1920,1080']
)
def setup_desctop_browser(request):
    options = Options()
    options.add_argument(f"window-size={request.param}")
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

    yield request.param

    browser.quit()

@pytest.fixture(
    params=['375,667']
)
def setup_mobile_browser(request):
    options = Options()
    options.add_argument(f"window-size={request.param}")
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

    yield request.param

    browser.quit()

def test_github_desktop(setup_desctop_browser):
    browser.open('/')

    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))


def test_github_mobile(setup_mobile_browser):
    browser.open('/')

    browser.element('.Button--link').click()
    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))


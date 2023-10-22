"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import browser, have
from selenium.webdriver.chrome.options import Options


@pytest.fixture(
    params=['1920,1080', '375,667']
)
def setup_browser(request):
    options = Options()
    options.add_argument(f"window-size={request.param}")
    browser.config.driver_options = options
    browser.config.base_url = 'https://github.com'

    yield

    browser.quit()

for_desktop = pytest.mark.parametrize('setup_browser', ['1920,1080'], indirect=True)
for_mobile = pytest.mark.parametrize('setup_browser', ['375,667'], indirect=True)

@for_desktop
def test_github_desktop(setup_browser):
    browser.open('/')

    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))

@for_mobile
def test_github_mobile(setup_browser):
    browser.open('/')

    browser.element('.Button--link').click()
    browser.element('[href="/login"]').click()

    browser.element('.auth-form-header h1').should(have.exact_text('Sign in to GitHub'))
# python-packages
My python packages


If you like what I do and want to buy me a cup of coffee. It is always appreciated :)

<a href="https://www.buymeacoffee.com/ij1qXRM6E" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Testing
Run ```py.test --cov-report term-missing --cov=smhi.smhi_lib``` and make sure we have no errors

# Make package
```python setup.py sdist```

# Pylint
```pylint smhi```
# Upload to pyint

```twine upload dist/*```

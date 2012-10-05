This is a [Sublime Text](sublime) package which generates and updates an ide helper for using SublimeCodeIntel with the Codeigniter framework.

## Installation ##

### With Package Control ###

If you have [Package Control][package_control] installed, you can install Codeigniter Codeintel Helper from inside Sublime Text itself. Open the Command Palette and select "Package Control: Install Package", then search for Codeigniter Codeintel Helper.

### Without Package Control ###

If you haven't got Package Control installed you will need to make a clone of this repository into your packages folder, like so:

    git clone https://github.com/speilberg0/ci-codeintel-helper.git "Codeigniter Codeintel Helper"


[sublime]: http://www.sublimetext.com/
[package_control]: http://wbond.net/sublime_packages/package_control

If you find error or wathever just fork it and send me a pull request.

## Usage ##

While working on a Codeigniter project, invoke the command palette and run

    CI Codeintel Helper: Create IDE helper

this should create a ci_ide_helper.php file in the base of your CI project to help SublimeCodeIntel offer completion.

## Options ##

- strip_model [true | false (default)] - add user models to helper with _model taken off the @property variable name

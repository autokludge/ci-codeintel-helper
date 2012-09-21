import os
import sublime
import sublime_plugin


class GenerateCodeintelHelperCommand(sublime_plugin.WindowCommand):
    def run(self):
        # get root folder
        folders = self.window.folders()
        for folder in folders:
            contents = os.listdir(folder)
            if 'application' in contents and 'system' in contents and 'index.php' in contents:
                self.root = folder
                break
        if not hasattr(self, 'root'):
            sublime.status_message('Could not find project root')
            return

        # get model names
        model_dirs = [x[0] for x in os.walk(os.path.join(self.root, 'application')) if 'models' in x[0]]
        models = []
        for model_dir in model_dirs:
            files = os.listdir(model_dir)
            for f in files:
                if f[-4:] == '.php':
                    models.append(f[:-4])

        # get base ide helper
        contents = open('ci_ide_helper.php').read()

        # add in user models
        settings = sublime.load_settings('CI Codeintel Helper.sublime-settings')
        strip_model = settings.get('strip_model')
        for model in models:
            model_class = ''.join([model[0].upper(), model[1:]])
            if strip_model:
                model_var = model.replace('_model', '')
            else:
                model_var = model

            rep = ' * @property %s $%s    User Defined model\n */\nc' % (model_class, model_var)
            contents = contents.replace(' */\nc', rep)

        # write helper file
        with open(os.path.join(self.root, 'ci_ide_helper.php'), 'w') as f:
            f.write(contents)

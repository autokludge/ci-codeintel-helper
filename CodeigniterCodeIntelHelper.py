import os
import sublime
import sublime_plugin
import ci_ide_helper


class GenerateCodeintelHelperCommand(sublime_plugin.WindowCommand):
    def run(self):
        # get base ide helper
        print 'start plugin'

        # content = open('ci_ide_helper.php').read()
        content = ci_ide_helper.contents

        # get root folder
        folders = self.window.folders()
        for folder in folders:
            contents = os.listdir(folder)
            if 'index.php' in contents:
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

        # add in user models
        rep = ' * ==============START USER DEFINED MODELS===============\n */\nc'
        content = content.replace(' */\nc', rep)

        settings = sublime.load_settings('CI Codeintel Helper.sublime-settings')
        strip_model = settings.get('strip_model')
        for model in models:
            model_class = ''.join([model[0].upper(), model[1:]])
            if strip_model:
                model_var = model.replace('_model', '')
            else:
                model_var = model

            rep = ' * @property %s $%s    User Defined model\n */\nc' % (model_class, model_var)
            content = content.replace(' */\nc', rep)

        print contents
        # write helper file
        with open(os.path.join(self.root, 'ci_ide_helper.php'), 'w') as f:
            f.write(content)

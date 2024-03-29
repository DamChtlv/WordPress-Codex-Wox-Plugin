Wox.Plugin.WordPressCodex
=====================

**Searching WordPress core documentation made easy.**  
Finding results is very fast because it searches in local JSON files (instead of an online API).
The JSON files included in this workflow are created with the [WP Parser JSON plugin](https://github.com/keesiemeijer/wp-parser-json)  

[![Screen 1](https://github.com/DamChtlv/WordPress-Codex-Wox-Plugin/blob/assets/Screenshots/screen1.png)](#screen1)  

Features
---------
You can search through all this and click to access rapidly on the WordPress reference page:
- ***Actions***: `wp action init`
- ***Classes***: `wp class wp query`
- ***Hooks***: `wp hook get term`
- ***Filters***: `wp filter edit term link`
- ***Functions***: `wp function get permalink`  

... or you can also **search randomly** like so: `wp get permalink`  
[![Screen 2](https://github.com/DamChtlv/WordPress-Codex-Wox-Plugin/blob/assets/Screenshots/screen2.png)](#screen2)  

Installation
---------
To install the plugin :
- Download the latest release of the plugin : https://github.com/DamChtlv/WordPress-Codex-Wox-Plugin/releases/latest/download/WordPress.Codex.zip
- Go to your folder `C:/Users/%USER%/AppData/Roaming/Wox/Plugins` then simply unzip the archive and you should have a folder named **WordPress Codex**  
*Should be something like: `C:/Users/%USER%/AppData/Roaming/Wox/Plugins/WordPress Codex/`*
- Restart **Wox** and type `Settings`
- Verify that you have correctly set the **Python** Path in **General** tab  
*Should be something like: `C:/Users/%user%/AppData/Local/Programs/Python/Python37/`*  
- Go to the **Plugin** tab and look for **WordPress Codex** plugin  
*If it doesn't show, either you put the plugin folder in the wrong directory or Wox can't find your python*
- Type `wp` in **Wox** & wait few secs *(you will see the loading occuring while it's checking / updating json files)*
- Enjoy ✌ 

Version
-------
*It's all based on **WordPress 5.4 Codex / Developer references*** at the moment  
*`Update` command allows to update json files to get latest version of codex reference.*

TODO
----
- ~~Allow random search without prefix: `wp get permalink` *(and maybe add type of reference in description of result)*~~  
- ~~Improve search algorithm, this should normally works: `wp function get title` *(by exploding each word and search for each of them a match with a scoring system)*~~
- Make my own json files from developer reference site *(to replace description by arguments of func, hooks... More interesting data)*
- Migrate this plugin to **[Flow Launcher](https://github.com/gabrielcarloto/flow-launcher-helper)**

Credits
---------
This is inspired by / fork of [Alfred WordPress Developer Workflow](https://github.com/keesiemeijer/alfred-wordpress-developer-workflow) (by [@keesiemeijer](https://github.com/keesiemeijer)) **for Wox (Windows)** written in Python

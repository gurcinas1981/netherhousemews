# Netherhouse Mews

Static property website for netherhousemews.foxatlas.co.uk.

## GitHub and Vercel

Import this repository into Vercel. Use the repository root as Root Directory and Other as the framework. The root vercel.json sets the output directory to dist and disables the build command. No dependency installation is required.

Connect the production branch to enable automatic deployments on pushes. Add netherhousemews.foxatlas.co.uk under the project’s Domains settings and use the exact DNS record Vercel supplies for this project. Domain activation and HTTPS must be confirmed after DNS verification.

## Website files

The complete website is in dist/. Keep media, fonts, vendor scripts and the HTML together. The supplied design runtime is a separate script because embedding it in index.html breaks the export’s template parser.

The Vimeo story uses video 1222793187. Its embed permissions must allow the production domain.

The .openai/hosting.json file identifies the existing private ChatGPT review site; Vercel serves only dist/.
